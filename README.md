# Problem Description

While hermetic Python toolchains are great for reproducible results, they incur a significant runtime overhead.
The reason for this is the large amount of symlinks which have to be created in the runfiles tree for the extracted Python interpreter together with the Python standard library.

You can modify the [WORKSPACE](./WORKSPACE) file to choose whether to use the host Python interpreter or a hermetic toolchain from rules_python.
The command `bazel run //:count_runfiles` shows you how many files and links exist in the runfiles tree.
The following table shows you the number for the runfile trees on  a Linux system.

| Python        | files and links in minimal runfiles tree |
|---------------|------------------------------------------|
| host Python   | 6                                        |
| hermetic 3.8  | 4532                                     |
| hermetic 3.9  | 4564                                     |
| hermetic 3.10 | 4584                                     |
| hermetic 3.11 | 4654                                     |
| hermetic 3.12 | 4600                                     |

# Impact on User

Creating such a large amount of symlinks has a cost one can clearly measure.
I did a non representative test with my system to showcase the impact.
Feel free to repeat the test with another system.

System:
- CPU: Intel, 24 cores (48 threads)
- Hard drive: SSD
- OS: Linux Mint 21.1
- Bazel: 7.0.0
- rules_pyhon: 0.27.0

The test command is `bazel test //...`.
It will execute 500 `py_test` targets.
Before each test a `bazel clean` has been performed and external dependencies like toolchains are already downloaded.
Time is measured by Bazel via the `Elapsed time: X.Xs, Critical Path: Y.Ys` output.

| Python        | Elapsed time |
|---------------|--------------|
| host Python   | 2.5 s        |
| hermetic 3.10 | 85 s         |

# Partial Mitigation

The issue is worsened Bazel being in a long migration phase for changing the layout of the runfiles dir.
For reference see:
- https://bazel.build/reference/command-line-reference#flag--legacy_external_runfiles
- https://github.com/bazelbuild/bazel/wiki/Updating-the-runfiles-tree-structure
- https://github.com/bazelbuild/bazel/issues/12821

Essentially, external dependencies are put twice into the runfiles tree, which doubles the impact of the large Python toolchain.

For my non representative test I can significantly reduce the overhead by disabling the legacy runfiles part.
`bazel test --nolegacy_external_runfiles //...`
reports an `Elapsed time` of 40 seconds, which is roundabout what we expect when halving the required links in the runfiles tree.

**In summary, one can reduce the hermetic Python toolchain overhead significantly by disabling the legacy runfiles tree structure with `--nolegacy_external_runfiles`**

# Further Notes

### Completely negating the issue

If it would be possible to put a symlink to the external directory containing the Python toolchain into the runfiles tree, there would be no extra cost for the hermeticity.
One would only pay for a single symlink instead of thousands.
If this is possible or violates central Bazel assumptions is unknown to me right now.

### This test is tailored to outline the problem

The test case we execute 500 times returns immediately on execution.
Thus, it puts an emphasis on the overhead introduced by using Bazel to run those tests.

Would those tests execute some real logic which requires time, the overhead of Bazel would be less impactful in a runtime measurement compared to the factor of 34 we demonstrate here.   
