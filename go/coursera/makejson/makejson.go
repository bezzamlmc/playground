package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

func main() {
	// Create a map to store addresses with name a key
	addresses := make(map[string]string)
	reader := bufio.NewReader(os.Stdin)

	var name, address string
	fmt.Println("Enter a name:")
	name, errn := read1Line(reader)
	if errn != nil {
		fmt.Println(errn)
		os.Exit(1)
	}
	fmt.Println("Enter the address:")
	address, erra := read1Line(reader)
	if erra != nil {
		fmt.Println(erra)
		os.Exit(2)
	}
	addresses["name"] = name
	addresses["address"] = address

	fmt.Println("JSON object text:")
	jsonAddresses, err := json.Marshal(addresses)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
	} else {
		fmt.Println(string(jsonAddresses))
	}
}

func read1Line(reader *bufio.Reader) (string, error) {
	s, e := reader.ReadString('\n')
	//fmt.Printf("full string %q\n", s)
	if e == nil {
		s = strings.TrimSuffix(s, "\r\n")
		s = strings.TrimSuffix(s, "\n")
		//		fmt.Printf("full string %q\n", s)
	}
	return s, e
}
