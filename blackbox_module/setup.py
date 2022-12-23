from distutils.core import setup, Extension


def main():
    setup(name="blackbox",
          version="0.0.0",
          description="Library for fast anomaly detection",
          author="DungyBug",
          author_email="",
          ext_modules=[Extension("blackbox", sources=["src/utils.cpp", "src/anomaly_detectors/delta_difference/delta_difference.cpp", "src/anomaly_detectors/linear_difference/linear_difference.cpp", "src/main.cpp"], extra_compile_args=["--std=c++2a"])])


if __name__ == "__main__":
    main()
