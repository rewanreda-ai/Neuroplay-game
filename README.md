# 🎮 NeuroPlay - Intelligent Cognitive Game Platform

An interactive, AI-powered cognitive game developed using Python and Pygame[cite: 1]. The platform is designed to test human cognitive abilities through multi-modal memory tasks while showcasing advanced Artificial Intelligence search and decision-making algorithms solving game states automatically.

---

## 🌟 Core Features
* Multi-Modal Gameplay (Human Modes):
  * Visual Mode: Players replicate generated color button sequences flashed on screen.
  * Audio Mode: Sequences are spoken out loud via text-to-speech engine, testing auditory memory.
  * Mixed Mode: Integrates both synchronized visual flashes and audio cues for advanced cognitive engagement.
* Agent Mode (AI Self-Play): Implements an automated AI agent capable of mimicking, computing, and successfully executing sequence solutions.
* Modern GUI: Clean UI styling featuring interactive buttons with smooth hover feedback built on Pygame.

---

## 🤖 Deployed AI Algorithms
In Agent Mode, players can select and observe three distinct algorithms processing game sequences:

1. Breadth-First Search (BFS): Explores all potential paths layer-by-layer to confidently track the correct historical sequence state.
2. A* Search Algorithm: Implements a fast heuristic-based search using path costs to quickly simulate and reproduce the sequence solution.
3. Minimax Algorithm: Simulates optimal structural steps by evaluating full operational depth recursively to ensure maximum point returns.

---

## 🛠️ Architecture & Technologies Used
* Language: Python
* GUI Framework: Pygame (Handling rendering pipelines, event ticking, and structural coordinate calculations).
* Audio Synthesis: pyttsx3 (Multithreaded Text-to-Speech implementation via Python native threads).
* Data Structures: collections.deque (Optimized double-ended queues for BFS traversal) and heapq (Binary heap priority queues for A* optimization).

---

## 💻 Setup & Execution

### Prerequisites
Ensure you have the required external libraries installed:
```bash
pip install pygame pyttsx3
