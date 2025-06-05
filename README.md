# x86-PTA

A python script to extract the x86 target features stored in GCC `gcc/config/i386/i386.h`.

Validated with GCC commit [dce4da51ab66c3abb84448326910cd42f6fe2499](https://github.com/gcc-mirror/gcc/commit/dce4da51ab66c3abb84448326910cd42f6fe2499).

## Usage

```bash
python3 x86-pta.py /path/to/gcc/config/i386/i386.h > x86-pta.csv
```

## Output

![output.svg](img/output.svg)
