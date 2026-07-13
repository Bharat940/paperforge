# Minimal Engrapha compilation script
import engrapha_notes as en

# Setup a clean default textbook theme
en.set_theme(en.TEXTBOOK)

# Add a simple cover card
en.cover_card(
    title="Getting Started with Engrapha",
    subtitle="A Minimal Example Document",
    author="Engrapha Developer",
    date="July 2026",
)
en.br()

# Add a header and table of contents
en.toc()

# Write some content
en.section("Hello World")
en.body("This is a minimal document compiled with the Engrapha Notes system.")
en.note("Tip: Run this file using python examples/getting_started.py to build the PDF.")

# Build the PDF
en.build_doc("getting_started.pdf")
print("Successfully generated getting_started.pdf")
