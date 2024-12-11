package main

import (
	"fmt"
	"net/http"

	"github.com/charmbracelet/glamour"
	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

func main() {
	http.HandleFunc("/ws", handleWebSocket)
	http.Handle("/", http.FileServer(http.Dir("../client")))

	fmt.Println("Server is running on :8080")
	http.ListenAndServe(":8080", nil)
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	conn, _ := upgrader.Upgrade(w, r, nil)
	defer conn.Close()

	// Use Glamour to render some markdown
	renderer, err := glamour.NewTermRenderer(
		glamour.WithStandardStyle("dark"),
	)
	if err != nil {
		fmt.Println(err)
		return
	}

	markdown := "# Welcome to the Terminal Game!\nThis is a *test* of **Glamour** with Go."
	styled, err := renderer.Render(markdown)
	if err != nil {
		fmt.Println(err)
		return
	}

	conn.WriteMessage(websocket.TextMessage, []byte(styled))

	for {
		// Handle messages or keep connection alive
		_, _, err := conn.ReadMessage()
		if err != nil {
			return
		}
	}
}
