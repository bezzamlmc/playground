package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	s "strings"
)

func main() {
	//Create a slice with an initial capacity of 3
	var slicei = make([]int32, 0, 3)

	var reader = bufio.NewReader(os.Stdin)

	var stringi string

	for {
		fmt.Println("Enter and integer or X to exit")
		//Note that ReadString will return the line as byte representation and the new line!
		line, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println(err)
			continue
		}
		fmt.Printf("full string %q\n", stringi)
		stringi = s.ToUpper(s.TrimSuffix(line, "\r\n"))
		if stringi == "X" {
			fmt.Println("Exiting program")
			break
		}
		inti, err := strconv.ParseInt(stringi, 10, 32)
		if err == nil {
			slicei = append(slicei, int32(inti))
			sort.Slice(slicei, func(i, j int) bool { return slicei[i] < slicei[j] })
			printSlice(slicei)
		} else {
			fmt.Println("Error parsing number. Please enter a valid integer")
		}
	}
}

func printSlice(s []int32) {
	fmt.Printf("length=%d capacity=%d %v\n", len(s), cap(s), s)
}
