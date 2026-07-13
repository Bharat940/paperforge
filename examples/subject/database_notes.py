# Database Notes Example
import engrapha_notes as en
import engrapha_diagrams as ed

en.set_theme(en.TEXTBOOK)

en.cover_preset(
    "database",
    title="Database Systems",
    subtitle="Unit II: Relational Model & Schema Design",
    author="Bharat Dangi",
    date="July 2026",
)
en.br()

en.toc()

theme = ed.DiagramTheme.from_notes_theme(en.get_theme())

en.part_box(
    "Relational Database Design",
    subtitle="Designing database schemas and defining table relationships",
    topics=["1. Entity Relationship Modeling", "2. Relational Schemas"],
)

en.chap_box("Chapter 1: Entity Relationship Modeling")
en.section("1.1 Customer-Order ER Relationship")
en.body(
    "We model a standard customer-orders database relationship where a customer places orders:"
)

# ER Diagram
er = ed.ERDiagram(
    width=en.CW, height=180, theme=theme, caption="Customer Orders ER Diagram"
)
er.entity("Customer")
er.entity("Order")
er.attribute("id", "Customer", pk=True)
er.attribute("name", "Customer")
er.attribute("order_no", "Order", pk=True)
er.attribute("amount", "Order")
er.relationship("places")
er.connect("Customer", "places", "1", "1")
er.connect("places", "Order", "1", "N")
en.add(er.as_flowable())
en.br()

en.chap_box("Chapter 2: Relational Schemas")
en.section("2.1 Database Tables Layout")
en.body("The ER diagram is mapped into relational database tables:")

# Relational Schema Diagram
schema = ed.SchemaDiagram(
    width=en.CW, height=220, theme=theme, caption="Relational Schema"
)
schema.table(
    "customers", [("id", "INT", {"pk": True}), ("name", "VARCHAR(100)", {})], x=50, y=30
)
schema.table(
    "orders",
    [
        ("order_no", "INT", {"pk": True}),
        ("customer_id", "INT", {"fk": True}),
        ("amount", "DECIMAL(10,2)", {}),
    ],
    x=280,
    y=30,
)
schema.relation("orders", "customer_id", "customers", "id")
en.add(schema.as_flowable())
en.br()

en.section("2.2 SQL Table Definition")
en.body("To implement this schema, we write SQL creation queries:")
en.code_block(
    """
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE orders (
    order_no INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
""",
    lang="sql",
)

en.build_doc("database_notes.pdf")
print("Successfully generated database_notes.pdf")
