# QR Code Pokémon Go Trade Site - MVP Scope

## Goal

Create a simple website where users can generate QR codes for their Pokémon Go friend codes and scan others' codes to add friends.

## Core Features

1. **Friend Code Input** – User can enter their Pokémon Go friend code (12-digit number).
2. **QR Code Generation** – The site generates a QR code representing the friend code.
3. **QR Code Display** – Show the QR code on screen for others to scan.
4. **Scan Simulation** – For testing, allow users to input a friend code from a scanned QR code (manual entry) to simulate scanning.
5. **Friend List** – Display a list of added friend codes (client-side only for MVP).
6. **Privacy** – No data is stored on a server; all data is kept in the browser (localStorage or sessionStorage) and cleared on exit.

## Constraints

- Do not use the official Pokémon Go logo or trademarked assets.
- The site is for educational/fun purposes only; not affiliated with Niantic or Pokémon.
- Include a disclaimer that the site is not official and usage is at user's own risk.
- No backend is required for MVP; all logic runs in the browser.

## Next Steps

- Create a simple HTML page with CSS and JavaScript.
- Implement friend code input and QR code generation using a library (e.g., QRCode.js).
- Add a display area for the QR code.
- Add a manual entry field to simulate scanning and add to friend list.
- Store friend list in localStorage.
- Add disclaimer and privacy notice.

## Validation Method

- The scope file exists (this file).
- A prototype can be built and runs locally in a browser.
