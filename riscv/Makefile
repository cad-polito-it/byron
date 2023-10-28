default:
	rm -rf $(name)
	riscv64-unknown-elf-as --warn --fatal-warnings -march=rv64imd -mno-relax $(name).s -o $(name).o
	riscv64-unknown-elf-ld --fatal-warnings -o $(name) $(name).o
	riscv64-unknown-elf-run --trace-register $(name)

clean:
	rm -rf $(name)