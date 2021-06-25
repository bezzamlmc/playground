package main

import {
	"fmt"
}

func main() {
	var f1 float32

	fmt.Printf("Enter a floating point number:\n")
	f1 = 8.2
	fmt.Scanf("%f", &f1)

	var if1 int32 = int32(f1)

	fmt.Printf("Floating point number is %f\nTruncated integer value is %d \n", f1, if1)
}
