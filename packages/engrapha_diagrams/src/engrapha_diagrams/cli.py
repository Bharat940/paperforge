"""
cli.py -- Command Line Interface for engrapha_diagrams documentation and guides.
"""

from __future__ import annotations

import argparse


def print_package_help() -> None:
    """Print comprehensive diagrams usage guide and API documentation to stdout."""
    guide = """================================================================================
                    ENGRAPHA DIAGRAMS DOCUMENTATION
================================================================================

Welcome to the engrapha_diagrams toolkit. This package provides a vector-native
PDF diagram library for ReportLab Platypus. All diagrams compile directly to
ReportLab Drawing objects that wrap seamlessly as Platypus Flowables.

--------------------------------------------------------------------------------
1. SUPPORTED DIAGRAM TYPES & PYTHON API
--------------------------------------------------------------------------------
- **Flowchart**:
  * Constructor: ed.Flowchart(width, height, theme=None, direction='TB', scale_factor=None)
  * Methods:
    .terminal(id, label)      - Oval terminal node
    .process(id, label)       - Rectangular process node
    .decision(id, label)      - Diamond decision node
    .io_box(id, label)        - Parallelogram input/output node
    .connector(id, label)     - Circle connector
    .predefined(id, label)    - Predefined process box node
    .edge(src, dst, label="", orthogonal=False, branch=None) - Link edge
  * Example:
    fc = ed.Flowchart(width=300, height=150, direction="LR")
    fc.terminal("start", "START").process("calc", "Calc").terminal("end", "END")
    fc.edge("start", "calc").edge("calc", "end")

- **Sequence Diagram**:
  * Constructor: ed.SequenceDiagram(width, height, theme=None)
  * Methods:
    .actor(id, label)         - Lifeline actor (person)
    .participant(id, label)   - Lifeline participant (box)
    .activate(id)             - Start activation bar
    .deactivate(id)           - End activation bar
    .message(src, dst, text, arrow='solid') - Message arrow ('solid', 'dashed', 'solid_open', 'dashed_open')
    .divider(text)            - Horizontal partition divider
  * Example:
    seq = ed.SequenceDiagram(width=400, height=220)
    seq.actor("c", "Client").actor("s", "Server")
    seq.activate("c").message("c", "s", "Request").activate("s")
    seq.message("s", "c", "Response", arrow="dashed").deactivate("s")

- **Layered Stack**:
  * Constructor: ed.LayeredStack(width, height, theme=None)
  * Methods:
    .layer(label, sublabel="") - Add a stack layer
    .divider()                 - Insert thick border line
  * Example:
    stack = ed.LayeredStack(width=300, height=150)
    stack.layer("Application", "HTTP").layer("Transport", "TCP")

- **Network Diagram**:
  * Constructor: ed.NetworkDiagram(width, height, theme=None)
  * Methods:
    .node(id, label, x, y, kind='host') - kinds: host, server, cloud, switch, database, router, firewall
    .link(id1, id2, label="")
  * Example:
    net = ed.NetworkDiagram(width=400, height=200)
    net.node("client", "PC", 50, 100).node("srv", "Server", 250, 100)
    net.link("client", "srv")

- **UML Class Diagram**:
  * Constructor: ed.ClassDiagram(width, height, theme=None, class_w=120)
  * Methods:
    .uml_class(id, name, stereotype="", attributes=[], methods=[])
    .relate(src, dst, kind='association', label="") - kinds: inheritance, realization, composition, aggregation, association, dependency
  * Example:
    cd = ed.ClassDiagram(width=300, height=200)
    cd.uml_class("Shape", "Shape", stereotype="abstract")
    cd.uml_class("Circle", "Circle", attributes=["- r: double"])
    cd.relate("Circle", "Shape", kind="inheritance")

- **Entity-Relationship Diagram (ER)**:
  * Constructor: ed.ERDiagram(width, height, theme=None)
  * Methods:
    .entity(id)
    .relationship(id)
    .entity_attributes(entity_id, attribute_list) - attribute_list elements: "Name" or ("ID", {"pk": True})
    .connect(node1, node2, card_from=None, card_to=None)
  * Example:
    er = ed.ERDiagram(width=400, height=180)
    er.entity("User").relationship("Owns").entity("Device")
    er.entity_attributes("User", [("ID", {"pk": True}), "Email"])
    er.connect("User", "Owns", card_from="1", card_to="N")

- **State Machine**:
  * Constructor: ed.StateMachine(width, height, theme=None)
  * Methods:
    .state(id, label, x, y, initial=False, accepting=False)
    .transition(src, dst, label="")
  * Example:
    sm = ed.StateMachine(width=300, height=150)
    sm.state("s0", "Init", 50, 75, initial=True).state("s1", "Done", 250, 75, accepting=True)
    sm.transition("s0", "s1", "process")

- **Timing Diagram**:
  * Constructor: ed.TimingDiagram(width, height, theme=None)
  * Methods:
    .clock(label, period, cycles)
    .signal(label, transitions) - transitions: list of (time, state_0_or_1)
  * Example:
    td = ed.TimingDiagram(width=400, height=120)
    td.clock("CLK", 20.0, 5).signal("RESET", [(0, 1), (15, 0)])

- **Database Schema Diagram**:
  * Constructor: ed.SchemaDiagram(width, height, theme=None)
  * Methods:
    .table(name, columns, x=0, y=0) - columns: list of (col_name, col_type, {"pk": True/False, "fk": True/False})
    .relation(table1, col1, table2, col2)
  * Example:
    schema = ed.SchemaDiagram(width=400, height=200)
    schema.table("users", [("id", "INT", {"pk": True}), ("name", "VARCHAR", {})])

- **Service Architecture Diagram**:
  * Constructor: ed.ArchitectureDiagram(width, height, theme=None, orientation='horizontal')
  * Methods:
    .client(id, label), .service(id, label), .database(id, label), .queue(id, label)
    .connect(src, dst, label="")
  * Example:
    arch = ed.ArchitectureDiagram(width=400, height=200)
    arch.client("client", "Browser").service("api", "API Gateway")
    arch.connect("client", "api", "HTTPS")

- **C4 Container Diagram**:
  * Constructor: ed.C4ContainerDiagram(width, height, theme=None)
  * Methods:
    .system(id, label, desc="")
    .container(id, label, technology, desc="")
    .relate(src, dst, label="")
  * Example:
    c4 = ed.C4ContainerDiagram(width=400, height=180)
    c4.system("user", "User").container("spa", "SPA", "React")
    c4.relate("user", "spa", "Uses")

- **Git Branch Flow**:
  * Constructor: ed.GitDiagram(width, height, theme=None)
  * Methods:
    .commit(branch, label)
    .branch(parent, child)
    .merge(from_branch, to_branch, label)
  * Example:
    git = ed.GitDiagram(width=300, height=120)
    git.commit("main", "Init").branch("main", "dev").commit("dev", "Feature")

- **AWS Diagram**:
  * Constructor: ed.AWSDiagram(width, height, theme=None, orientation='horizontal')
  * Methods:
    .ec2(id, label), .rds(id, label), .s3(id, label), .lambda_fn(id, label), .sqs(id, label)
    .connect(src, dst, label="")
  * Example:
    aws = ed.AWSDiagram(width=400, height=200)
    aws.ec2("web", "Instance").rds("db", "RDS")
    aws.connect("web", "db", "SQL Connection")

--------------------------------------------------------------------------------
2. STANDALONE EXPORT & FORMATS
--------------------------------------------------------------------------------
Export any drawing directly to vector or raster formats without a ReportLab story:
  fc.save("flowchart.pdf")  # PDF vector
  fc.save("flowchart.svg")  # SVG vector
  fc.save("flowchart.png")  # PNG raster
  fc.save("flowchart.jpg")  # JPG raster

--------------------------------------------------------------------------------
3. DIAGRAM THEMES
--------------------------------------------------------------------------------
Apply presets or inherit from the active notes theme:
  # 1. Preset themes
  fc = ed.Flowchart(width=300, height=200, theme=ed.LIGHT) # ed.DARK also available

  # 2. Inherit from active notes theme
  en.set_theme(en.OCEAN_DARK)
  theme = ed.DiagramTheme.from_notes_theme(en.get_theme())
  fc = ed.Flowchart(width=300, height=200, theme=theme)

  # 3. Custom theme parameters available in ed.DiagramTheme:
  #    bg, text, node_fill, node_stroke, node_text, arrow_color, font_name, etc.

--------------------------------------------------------------------------------
4. INTEGRATION WITH ENGRAPHA_NOTES
--------------------------------------------------------------------------------
To embed any diagram into a ReportLab story, call `.as_flowable()` and pass the
result to `en.add()`. This flattens the drawing along with its optional caption:

  import engrapha_notes as en
  import engrapha_diagrams as ed

  # Create a diagram
  fc = ed.Flowchart(width=en.CW, height=180)
  fc.terminal("s", "START").terminal("e", "END").edge("s", "e")

  # Add it to the story flow
  en.add(fc.as_flowable())

--------------------------------------------------------------------------------
5. CLI USAGE
--------------------------------------------------------------------------------
Show this API reference:
  engrapha-diagrams [--info]

--------------------------------------------------------------------------------
6. MARKDOWN DSL SYNTAX REFERENCE
--------------------------------------------------------------------------------
In Markdown compiler mode, you can embed diagrams using fenced blocks with the
following syntax patterns:

- **flowchart**:
  ```flowchart
  width=400
  height=180
  direction=LR
  terminal start "START"
  process calc "Calc"
  decision check "check"
  terminal end "END"
  edge start calc
  edge calc check
  edge check end "yes"
  edge check calc "no" orthogonal=true
  ```

- **sequence**:
  ```sequence
  actor c "Client"
  participant s "Server"
  message c s "GET /"
  divider "Server logic"
  message s c "200 OK"
  ```

- **layeredstack**:
  ```layeredstack
  layer "Application" "HTTP"
  layer "Transport" "TCP"
  divider
  layer "Network" "IP"
  ```

- **schema**:
  ```schema
  table users x=50 y=100
    id: INT (pk)
    email: VARCHAR
  table orders x=250 y=100
    id: INT (pk)
    user_id: INT (fk) -> users.id
  ```

- **git**:
  ```git
  commit main "Initial"
  branch main feature
  commit feature "Task"
  merge feature main "Done"
  ```

- **architecture**:
  ```architecture
  client web "Browser"
  service api "Backend"
  database db "MySQL"
  connect web api "HTTPS"
  connect api db "SQL"
  ```

- **aws**:
  ```aws
  ec2 web "Instance"
  rds db "Database"
  connect web db "Link"
  ```

- **c4**:
  ```c4
  system user "Customer"
  container app "SPA" "React"
  relate user app "Uses"
  ```

All commands inside code blocks are case-insensitive and parse parameter fields
separated by spaces or quotation marks.
================================================================================"""
    print(guide)


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="CLI documentation reference for engrapha_diagrams toolkit."
    )
    parser.add_argument(
        "--info",
        "-i",
        action="store_true",
        help="Print comprehensive diagrams usage guide and API documentation.",
    )

    parser.parse_args()

    # Default to print info if run standalone
    print_package_help()


if __name__ == "__main__":
    main()
