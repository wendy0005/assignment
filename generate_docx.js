const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, BorderStyle, WidthType, ShadingType } = require('docx');
const fs = require('fs');

const doc = new Document({
    styles: {
        default: {
            document: {
                run: {
                    font: "Arial",
                    size: 24, // 12pt
                },
            },
        },
        paragraphStyles: [
            {
                id: "Heading1",
                name: "Heading 1",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: {
                    size: 32,
                    bold: true,
                    font: "Arial",
                },
                paragraph: {
                    spacing: { before: 240, after: 240 },
                    outlineLevel: 0,
                },
            },
            {
                id: "Heading2",
                name: "Heading 2",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: {
                    size: 28,
                    bold: true,
                    font: "Arial",
                },
                paragraph: {
                    spacing: { before: 180, after: 180 },
                    outlineLevel: 1,
                },
            },
        ],
    },
    sections: [{
        properties: {
            page: {
                size: {
                    width: 11906, // A4
                    height: 16838,
                },
                margin: {
                    top: 1440,
                    right: 1440,
                    bottom: 1440,
                    left: 1440,
                },
            },
        },
        children: [
            new Paragraph({
                text: "Computer Architecture Assignment (BIT2233/BTL2333/BCL2233)",
                heading: HeadingLevel.HEADING_1,
                alignment: AlignmentType.CENTER,
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "Student Name: [Your Name]", break: 1 }),
                    new TextRun({ text: "Student ID: [Your ID]", break: 1 }),
                    new TextRun({ text: "Programme: [Your Programme]", break: 1 }),
                    new TextRun({ text: "Course Code: BIT2233/BTL2333/BCL2233", break: 1 }),
                    new TextRun({ text: "Lecturer’s Name: [Lecturer's Name]", break: 1 }),
                    new TextRun({ text: "Date: 18 March 2026", break: 1 }),
                ],
            }),

            new Paragraph({ text: "PART A: Instruction Set Architecture (ISA) Analysis", heading: HeadingLevel.HEADING_2 }),
            new Paragraph({
                text: "The Instruction Set Architecture (ISA) serves as the foundational interface between a computer's hardware and its software, defining the repertoire of operations a processor can execute. In modern computing, the architectural landscape is dominated by two primary philosophies: Reduced Instruction Set Computer (RISC) and Complex Instruction Set Computer (CISC). The RISC approach, exemplified by ARM architectures, focuses on a small, highly optimized set of instructions designed to execute in a single clock cycle. By utilizing fixed-length instruction formats, RISC simplifies the fetch and decode stages, which in turn facilitates high-efficiency pipelining. Furthermore, RISC systems adhere to a strict load/store architecture, where arithmetic operations are confined to internal registers and memory access is limited to specific instructions.",
            }),
            new Paragraph({
                text: "Conversely, the CISC philosophy, represented by the x86 architecture, emphasizes providing a versatile array of complex instructions. These commands can often perform multiple low-level operations—such as loading from memory, performing an addition, and storing the result—within a single high-level instruction. While this approach allows for more compact code and efficient memory usage, the variable-length nature of CISC instructions increases the complexity of the decoding hardware. From a design perspective, the choice between these architectures involves a trade-off between power efficiency and raw processing flexibility.",
            }),
            new Paragraph({
                text: "The practical interaction between these instructions and CPU components is best observed through a specific sequence of operations designed to compute A = B + C. Consider the following instruction list:",
            }),
            new Paragraph({ text: "1. LDR R1, B: The processor fetches the value from memory address B and loads it into register R1 via the Data Bus.", indent: { left: 720 } }),
            new Paragraph({ text: "2. LDR R2, C: Similarly, the value at address C is retrieved and stored in register R2.", indent: { left: 720 } }),
            new Paragraph({ text: "3. ADD R3, R1, R2: The Control Unit (CU) decodes the opcode and signals the Arithmetic Logic Unit (ALU) to sum the contents of R1 and R2, storing the result in R3.", indent: { left: 720 } }),
            new Paragraph({ text: "4. STR R3, A: Finally, the calculated value in R3 is written back to memory address A.", indent: { left: 720 } }),

            new Paragraph({ text: "PART B: Number Conversion & Data Representation", heading: HeadingLevel.HEADING_2 }),
            new Paragraph({ text: "1. Decimal to Binary Conversion", bold: true }),
            new Paragraph({ text: "To convert 28.625 to binary: Integer part 28 = 11100. Fractional part 0.625 = .101. Final Result: 11100.101." }),
            new Paragraph({ text: "2. Binary to Hexadecimal Conversion", bold: true }),
            new Paragraph({ text: "11011011 grouped as (1101) and (1011) results in DB in hexadecimal." }),
            new Paragraph({ text: "3. Eight-Bit Two’s Complement Arithmetic", bold: true }),
            new Paragraph({ text: "12 - 5 results in 00000111 (binary 7)." }),
            new Paragraph({ text: "4. Floating Point Interpretation", bold: true }),
            new Paragraph({ text: "1.110 x 2^3 results in decimal 14.0." }),

            new Paragraph({ text: "PART C: Logic Gates & Digital Logic Understanding", heading: HeadingLevel.HEADING_2 }),
            new Paragraph({
                text: "The implementation of automated systems, such as a smart greenhouse irrigation controller, relies heavily on the logical behavior of AND, OR, NOT, and XOR gates. The primary logic requires the water pump (Y) to activate if both the soil is dry (A) and the temperature is high (B)—an automated trigger—or if the farmer manually engages the override (C). This is represented by Y = (A · B) + C.",
            }),

            new Paragraph({ text: "PART D: Processor Organisation Analysis", heading: HeadingLevel.HEADING_2 }),
            new Paragraph({
                text: "The internal organization of a processor is a highly coordinated environment where the Control Unit (CU), Arithmetic Logic Unit (ALU), and registers work in tandem via a system of buses. The CU acts as the coordinator, fetching and decoding instructions, while the ALU performs mathematical operations. Data flows through the Data Bus, while the Address Bus specifies locations in memory.",
            }),

            new Paragraph({ text: "PART E: CPU Cycle & Performance Calculation", heading: HeadingLevel.HEADING_2 }),
            new Paragraph({ text: "Clock Rate: 2.5 GHz | Instructions: 5 x 10^8 | CPI: 1.8" }),
            new Paragraph({ text: "1. Clock Cycle Time (T) = 1 / 2.5GHz = 0.4 ns", bold: true }),
            new Paragraph({ text: "2. Total Execution Time = (5x10^8) * 1.8 * 0.4ns = 0.36 seconds", bold: true }),

            new Paragraph({ text: "PART F: Pipeline & Hazard Analysis", heading: HeadingLevel.HEADING_2 }),
            new Paragraph({
                text: "Pipelining overlaps instruction execution to increase throughput. However, it is limited by hazards: Structural (resource conflicts), Data (logic dependencies), and Control (branching issues). Modern processors use data forwarding and branch prediction to mitigate these stalls.",
            }),

            new Paragraph({ text: "REFERENCES", heading: HeadingLevel.HEADING_2 }),
            new Paragraph({ text: "Hennessy, J. L., & Patterson, D. A. (2017). Computer Architecture: A Quantitative Approach (6th ed.)." }),
            new Paragraph({ text: "Flynn, M. J., & Hung, P. (2015). Performance Factors for Superscalar Processors. IEEE." }),
            new Paragraph({ text: "Omondi, A. (2023). The Microarchitecture of Pipelined and Superscalar Computers. Springer." }),
        ],
    }]
});

Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync("Computer_Architecture_Assignment.docx", buffer);
    console.log("DOCX successfully generated.");
});
