//--------------------------------|###|------------------------------------//
//  __                            |   |                                    //
// |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    //
// |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer //
// |_____|___  |__| |_____|__|__|  ).(  https://github.com/cad-polito-it/byron //
//       |_____|                   \|/                                     //
//--------------------------------- ' -------------------------------------//
// Copyright 2023 Giovanni Squillero and Alberto Tonda
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
