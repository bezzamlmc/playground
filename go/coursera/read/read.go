package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Name struct {
	fname string
	lname string
}

func main() {
	var fileName, token1, token2 string

	var nameSlice []Name
	nameSlice = make([]Name, 0, 5)

	fmt.Println("Enter a file name:")
	fmt.Scan(&fileName)

	file, err := os.Open(fileName)

	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	scanner := bufio.NewScanner(file)

	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		line := scanner.Text()

		tokens := strings.Split(line, " ")

		token1 = truncate(tokens[0], 20)
		token2 = truncate(tokens[1], 20)

		nameSlice = append(nameSlice, Name{fname: token1, lname: token2})
	}

	for _, nm := range nameSlice {
		fmt.Printf("First name:%s; Last name: %s\n", nm.fname, nm.lname)
	}

}

func truncate(s string, length int) string {
	if len(s) > length {
		s = s[0:length]
	}
	return s
}
