load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "9acc0944c94adb23fba1c9988b48768b1bacc6583b52a2586895c5b7491e2e31",
    strip_prefix = "rules_python-0.27.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.27.0/rules_python-0.27.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

# Comment this for fast execution with host Python interpreter
python_register_toolchains(
    name = "hermetic_python",
    python_version = "3.10",
)
