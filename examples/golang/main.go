//=================================|===|===================================//
//  _____                          |   |                                   //
// |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   //
// |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. //
// |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         //
//       |_____|                    \|/                                    //
//================================== ' ====================================//
// Copyright 2023-25 Giovanni Squillero and Alberto Tonda
// SPDX-License-Identifier: Apache-2.0

package main

import "fmt"

func main() {
	num := evolved_function()

	var bits uint64
	for num != 0 {
		bits += num & uint64(0x1)
		num >>= 1
	}
	fmt.Println(bits)

}
