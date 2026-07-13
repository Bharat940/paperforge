# Vector Diagrams Showcase
import engrapha_notes as en
import engrapha_diagrams as ed

# Setup a clean default textbook theme
en.set_theme(en.TEXTBOOK)

en.cover_preset(
    "engineering",
    title="Vector Diagrams Showcase",
    subtitle="Flowcharts, State Machines, Sequence, & ER Diagrams",
    author="Bharat Dangi",
    date="July 2026",
)
en.br()

en.toc()

# Use notes theme to build diagram theme
theme = ed.DiagramTheme.from_notes_theme(en.get_theme())

# ---------------------------------------------------------
en.section("1. Flowchart Builder")
en.body("Flowcharts define process branches and logic sequences:")

fc = ed.Flowchart(width=en.CW, height=220, theme=theme, caption="Flowchart Example")
fc.terminal("start", "START")
fc.decision("check", "Condition?")
fc.process("yes_path", "Action Yes")
fc.process("no_path", "Action No")
fc.terminal("end", "END")

fc.edge("start", "check")
fc.edge("check", "yes_path", label="Yes")
fc.edge("check", "no_path", label="No")
fc.edge("yes_path", "end")
fc.edge("no_path", "end")

en.add(fc.as_flowable())
en.br()

# ---------------------------------------------------------
en.section("2. State Machine Builder")
en.body("State machines show state transitions and events:")

sm = ed.StateMachine(
    width=en.CW, height=150, theme=theme, caption="State Machine Example"
)
sm.state("s0", "Idle", initial=True)
sm.state("s1", "Active")
sm.state("s2", "Done", accepting=True)

sm.transition("s0", "s1", label="start")
sm.transition("s1", "s1", label="working")
sm.transition("s1", "s2", label="complete")

en.add(sm.as_flowable())
en.br()

# ---------------------------------------------------------
en.section("3. Sequence Diagram Builder")
en.body("Sequence diagrams model call flows and message lifetimes:")

seq = ed.SequenceDiagram(
    width=en.CW, height=200, theme=theme, caption="Sequence Diagram Example"
)
seq.actor("client", "Client")
seq.actor("server", "Server")
seq.actor("db", "Database")

seq.message("client", "server", "GET /user/12")
seq.activate("server")
seq.message("server", "db", "SELECT *")
seq.message("db", "server", "User Data", arrow="dashed")
seq.message("server", "client", "200 OK", arrow="dashed")
seq.deactivate("server")

en.add(seq.as_flowable())
en.br()

# ---------------------------------------------------------
en.section("4. Entity Relationship (ER) Diagram")
en.body("ER Diagrams model tables and column metadata relationships:")

er = ed.ERDiagram(width=en.CW, height=180, theme=theme, caption="ER Diagram Example")
er.entity("Customer")
er.entity("Address")
er.attribute("cust_id", "Customer", pk=True)
er.attribute("name", "Customer")
er.attribute("addr_id", "Address", pk=True)
er.relationship("has")
er.connect("Customer", "has", "1", "1")
er.connect("has", "Address", "1", "N")

en.add(er.as_flowable())

en.build_doc("diagrams.pdf")
print("Successfully generated diagrams.pdf")
