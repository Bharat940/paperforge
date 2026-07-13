# Networking Notes Example
import engrapha_notes as en
import engrapha_diagrams as ed

# Setup a clean default textbook theme
en.set_theme(en.TEXTBOOK)

en.cover_preset(
    "networking",
    title="Computer Networks",
    subtitle="Unit IV: Transport Layer & TCP Handshake",
    author="Bharat Dangi",
    date="July 2026",
)
en.br()

en.toc()

theme = ed.DiagramTheme.from_notes_theme(en.get_theme())

en.part_box(
    "Unit IV: Transport Layer",
    subtitle="Transport service models, TCP congestion control, and connection management",
    topics=["1. TCP Service Model", "2. TCP Connection Management"],
)

en.chap_box("Chapter 1: TCP Service Model")
en.section("1.1 TCP Segment Format")
en.body(
    "TCP is a connection-oriented, reliable byte-stream protocol. "
    "The diagram below shows the header format stack representing the packet encapsulation:"
)

# Layered Stack Diagram representing packet layers
stack = ed.LayeredStack(width=300, height=150, theme=theme, caption="TCP Packet Layers")
stack.layer("Application Layer (HTTP, DNS)")
stack.layer("Transport Layer (TCP Segment)")
stack.layer("Network Layer (IP Datagram)")
stack.layer("Link Layer (Ethernet Frame)")
en.add(stack.as_flowable())
en.br()

en.chap_box("Chapter 2: TCP Connection Management")
en.section("2.1 TCP Three-Way Handshake")
en.body(
    "To establish a connection, TCP uses a three-way handshake: "
    "1. Client sends SYN. 2. Server responds with SYN-ACK. 3. Client acknowledges with ACK."
)

# Sequence Diagram representing Handshake
seq = ed.SequenceDiagram(
    width=en.CW, height=220, theme=theme, caption="TCP Handshake Flow"
)
seq.actor("client", "Client (Initiator)")
seq.actor("server", "Server (Listener)")

seq.message("client", "server", "SYN (seq=x)")
seq.activate("server")
seq.message("server", "client", "SYN-ACK (seq=y, ack=x+1)", arrow="dashed")
seq.message("client", "server", "ACK (seq=x+1, ack=y+1)")
seq.deactivate("server")

en.add(seq.as_flowable())

en.build_doc("networking_notes.pdf")
print("Successfully generated networking_notes.pdf")
