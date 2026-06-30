# Compiling Byte

## Requirements

- **C++ Compiler**: GCC or Clang with C++17 support
- **Disk Space**: ~500 MB (with training data)
- **Libraries**: Standard C++ library only (no external dependencies)

### Platform Support

| Platform | Compiler | Command |
|----------|----------|---------|
| Linux | g++ | `g++ -std=c++17 Byte.cpp -o Byte` |
| macOS | clang | `clang++ -std=c++17 Byte.cpp -o Byte` |
| Windows | g++ (MinGW) | `g++ -std=c++17 Byte.cpp -o Byte.exe` |

## Quick Compile

### Simple One-Liner
```bash
g++ -std=c++17 Byte.cpp -o Byte
```

### With Optimization (Faster Execution)
```bash
g++ -std=c++17 -O2 Byte.cpp -o Byte
```

### With Debug Symbols (For Debugging)
```bash
g++ -std=c++17 -g Byte.cpp -o Byte
```

## Verify Compilation

Check that the executable was created:
```bash
ls -lh Byte
```

Should show:
```
-rwxr-xr-x  1 user  staff  398K Jun 30 Byte
```

## Run After Compiling

```bash
./Byte
```

On Windows:
```bash
Byte.exe
```

## Compilation Options Explained

| Flag | Purpose |
|------|---------|
| `-std=c++17` | Use C++17 standard (required) |
| `-O2` | Optimize for speed (optional) |
| `-g` | Include debug symbols (optional) |
| `-Wall` | Show all warnings (optional) |
| `-Werror` | Treat warnings as errors (optional) |

## Full Command with All Options

```bash
g++ -std=c++17 -O2 -Wall Byte.cpp -o Byte
```

## Troubleshooting

### "g++: command not found"
Install GCC:
- **Ubuntu/Debian**: `sudo apt-get install build-essential`
- **macOS**: `xcode-select --install`
- **Windows**: Download [MinGW](https://www.mingw-w64.org/)

### "error: C++17 not supported"
Update your compiler to a newer version:
- GCC 5.0+ supports C++17
- Clang 3.5+ supports C++17

### Compilation takes too long
Use `-O2` optimization flag or split compilation:
```bash
g++ -std=c++17 -O2 Byte.cpp -o Byte
```

## File Size

- **Debug build**: ~2 MB
- **Release build** (with -O2): ~398 KB
- **Stripped build**: ~150 KB

## Creating a Makefile (Optional)

Create a `Makefile` in the root directory:

```makefile
CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall
TARGET = Byte
SRC = Byte.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
```

Then compile with:
```bash
make          # Compile
make run      # Compile and run
make clean    # Remove executable
```

## Verify Everything Works

After compiling, test the bot:
```bash
echo "hello" | ./Byte
```

Should see:
```
📚 Loading training data...
...
🤖 BYTE - AI Knowledge Bot
```

---

**Questions?** Check [README.md](../README.md) or [CLAUDE.md](../CLAUDE.md)
