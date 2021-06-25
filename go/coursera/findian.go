package main

import (
	"fmt"
	s "strings"
)

func main() {
	var texto string
	fmt.Println("Enter a string:")
	fmt.Scanf("%s", &texto)
	var ltexto string = s.ToLower(texto)
	if s.HasPrefix(ltexto, "i") && s.Contains(ltexto, "a") && s.HasSuffix(ltexto, "n") {
		fmt.Println("Found!")
	} else {
		fmt.Println("Not found!")
	}
}
