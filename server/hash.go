package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"golang.org/x/crypto/bcrypt"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	// Step 1: Ask the user for a password
	fmt.Print("Enter a password: ")
	password, _ := reader.ReadString('\n')
	password = strings.TrimSpace(password)

	// Step 2: Hash the password
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		fmt.Println("Error hashing password:", err)
		return
	}

	fmt.Println("\nYour hashed password is:")
	fmt.Println(string(hashedPassword))

	// Step 3: Ask the user to enter their password again
	fmt.Print("\nType your password again: ")
	passwordAgain, _ := reader.ReadString('\n')
	passwordAgain = strings.TrimSpace(passwordAgain)

	// Step 4: Compare the new input with the hashed password
	err = bcrypt.CompareHashAndPassword(hashedPassword, []byte(passwordAgain))
	if err != nil {
		fmt.Println("\nPassword does not match!")
	} else {
		fmt.Println("\nPassword matches!")
	}
}
