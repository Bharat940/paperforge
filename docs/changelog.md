# Changelog

All notable changes to Engrapha are documented here. Engrapha follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### In progress

- Documentation website (mkdocs + Material)

## [0.1.1] - 2026-07-06

### Added
- **Cover Page Raster Image Support:** Added native support for PNG, JPG, and JPEG files on cover page logo and banner elements. Dimensions are automatically inspected using `ImageReader` to calculate scale heights proportionally, preserving image aspect ratio.
- **Balanced Cover Page Spacing:** Implemented dynamic top-margin scaling on the cover page when a logo is active to prevent the main title from being pushed too far down, maintaining a balanced, professional first-page layout.
- **State Machine Rendering Aesthetics:** Improved state transition diagram layouts by introducing symmetric self-loop arcs with solid arrowheads, centered labels, and automatic centerline alignment for sequential state chains. Bidirectional and skipped-node transition arcs have been made sleeker and more balanced.

### Fixed
- **Preset Property Forwarding:** Fixed a configuration forwarding issue in `cover_preset` to ensure custom banner, logo, and alignment configurations are correctly passed to `cover_card` instead of being dropped. Added `**extra` to `cover_card` to absorb and ignore legacy layout parameters (such as `meta`) passed by preset templates.
- **Layout and Typography Enhancements:** Resolved ReportLab's layout spacing gaps around inline equations and code fragments by updating the default paragraph alignment for body, definition, and proof blocks to left-alignment (`TA_LEFT`).
- **State Machine Overlaps:** Excluded self-loops from rank dependency layout calculations to ensure correct horizontal positioning, keeping start-state marker arrows cleanly separated from self-loops.

### Documentation
- **Command Line Interface Reference:** Expanded docstrings and readmes across all package packages to detail available CLI aliases (e.g. `engrapha`, `engrapha-diagrams`) and CLI flags (e.g. `--info`).

## [0.1.0] - 2026

Initial public release of Engrapha. Both packages contain feature-complete implementations:

### Engrapha Diagrams — `engrapha_diagrams`
- **Flowchart**: ANSI/ISO shapes with orthogonal routing
- **SequenceDiagram**: UML sequence with activation bars
- **ClassDiagram**: UML class with inheritance, composition, etc.
- **ERDiagram**: Chen notation with primary keys, multi-valued attributes
- **StateMachine**: DFA/NFA with initial/accepting state markers
- **NetworkDiagram**: hosts, servers, switches, clouds, topologies
- **ArchitectureDiagram**: clients, services, databases, queues
- **C4ContainerDiagram**: System / Container / relations
- **AWSDiagram**: vector-native EC2, RDS, S3, Lambda, SQS icons
- **GitDiagram**: branches, commits, merges
- **SchemaDiagram**: tables with foreign keys
- **TimingDiagram**: digital waveforms
- **LayeredStack**: OSI / TCP-IP / memory hierarchy
- 10 preset themes + custom theme support
- `DiagramTheme.from_notes_theme()` for theme matching
- Vector-native PDF/SVG/PNG export

### Engrapha Notes — `engrapha_notes`
  - 15 preset themes + ThemeBuilder + print-light theme
  - Cover cards, part / chap / section / subsection blocks
  - Callouts: tip, note, warning, important, exam, theorem, proof
  - Question blocks, qbox, answer, mcq, revision_card
  - Flashcards with Anki APKG / CSV / JSON export
  - Tables, code blocks with Pygments syntax highlighting
  - Formula / formula_block (LaTeX math via matplotlib mathtext)
  - Image with remote caching & fallbacks
  - Frame and packet format helpers (Ethernet, IPv4 header)
  - Multiple page numbering styles
  - Running headers and footers
  - TOC, bookmarks, footnotes, indices
  - Markdown CLI compiler
  - 4 export formats: PDF, HTML, PPTX, multiple-from-one document

### Security

  - No external network or binaries required
  - No raster fallbacks
  - Standard fonts only by default

