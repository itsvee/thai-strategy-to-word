---
name: thai-strategy-to-word
description: Build evidence-based reports from instructor requirements.
version: 0.2.0
author: Vixtrz, OpenAI Codex
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [strategy, report, interview, Thai, sustainability, HTML, Word]
    related_skills: []
---

# Thai Strategy to Word

ช่วยเปลี่ยนโจทย์อาจารย์ ข้อมูลบริษัท หลักฐานสาธารณะ ข้อมูลจากผู้ใช้ และ feedback ให้เป็นรายงานที่ตรวจย้อนกลับได้ ใช้กับทุกอุตสาหกรรมและไม่สมมติบริบทบริษัทใดเป็นค่าเริ่มต้น รายงานหลักเป็น HTML; สร้าง Word ด้วย runtime ที่ฝังไว้เมื่อผู้ใช้หรือโจทย์กำหนด

## When to Use

- ผู้ใช้ต้องทำรายงานเชิงกลยุทธ์ ความยั่งยืน หรือรายงานตามโจทย์อาจารย์
- ผู้ใช้ยังไม่เข้าใจโจทย์อาจารย์ หรือต้องการแปลง brief/rubric/feedback เป็นแผนเขียน
- ผู้ใช้มีรายงานเดิมและต้องแก้ตาม feedback
- ผู้ใช้ต้องการรายงาน HTML หรือ Word ภาษาไทย

ไม่ใช้เพื่อรับรองกฎหมาย อนุมัติแทนองค์กร หรือพยากรณ์การเงินจากข้อมูลที่ไม่มี

## Prerequisites

อ่าน `workflows/first-run.md` ก่อนเริ่มงานใหม่ อ่าน [interview.md](references/interview.md), [readiness.md](references/readiness.md), [evidence.md](references/evidence.md) และ [verification.md](references/verification.md) ตามจังหวะของงาน

ผู้ใช้เริ่มจากศูนย์ได้ ไม่ต้องรู้ชื่อ Framework และไม่ต้องติดตั้งตัวสร้าง Word เพิ่ม Python 3.11+ ใช้ readiness gate และ `vendor/thai-docx-upstream/` เป็น runtime Word ที่ฝังใน repository

## First-run workflow

1. **เริ่มจากผู้ใช้**: อ่าน `references/course-requirements.md` ซึ่งรวมคำถามแปดข้อและ feedback แบบไม่ผูกบริษัทไว้แล้ว ถามว่าผู้ใช้ทำงานที่ไหน ธุรกิจอะไร และรับผิดชอบส่วนใด ไม่ต้องขอให้ส่งโจทย์เดิมซ้ำ ถ้ามีคำสั่งหรือ feedback เพิ่ม ให้รับมาแก้ข้อกำหนดเฉพาะงาน
2. **สรุป Assignment Contract**: แยกคำถามที่ต้องตอบ, audience, genre, ภาษา, ความยาว, deadline, Framework, citation, ข้อห้าม และไฟล์ส่งเป็น `required`, `conditional`, `optional` หรือ `unknown`
3. **รับข้อมูลบริษัท**: ถามธุรกิจ ลูกค้า ขอบเขต บทบาทของผู้ใช้ ปัญหา เหตุการณ์จริง ผลที่ต้องการ ข้อจำกัด และสิ่งที่ยอมแลก
4. **เลือกเส้นทาง**: Discovery เมื่อยังไม่มีปัญหาชัด, Revision เมื่อมีรายงานหรือ feedback, Direct brief เมื่อโจทย์พร้อม
5. **ค้นและจัดหลักฐาน**: ค้นแหล่งปฐมภูมิของบริษัทและอุตสาหกรรม เพิ่มข้อมูลผู้ใช้โดยติดป้ายสถานะ แยกข้อเท็จจริง สมมติฐาน ข้อเสนอ และ unknown
6. **สร้าง Coverage Plan**: จับคู่ข้อกำหนดทุกข้อกับตำแหน่งในรายงาน หลักฐาน Framework ข้อสรุป ผลต่อการตัดสินใจ และข้อจำกัด
7. **ผ่าน readiness และยืนยันโจทย์**: ห้ามร่างเต็มก่อน `readiness_gate.py` พร้อมและผู้ใช้ยืนยันสรุปโจทย์ปัจจุบัน
8. **วิเคราะห์**: เลือก Framework ตามการตัดสินใจ ไม่ทำตารางให้ครบเฉย ๆ ทุก Framework ต้องมีข้อค้นพบ เหตุผล ทางเลือก ผลต่อทรัพยากร และข้อจำกัด
9. **เขียนรายงาน**: ใช้รูปแบบที่ Assignment Contract กำหนด หัวข้อเป็น statement เมื่อโจทย์ห้ามหัวข้อคำถาม รักษา narrative และกลุ่มผู้อ่านตาม brief/feedback
10. **ตรวจและส่งออก**: รัน coverage gate, ตรวจหลักฐานและความสอดคล้อง, สร้าง `report.html`, `coverage.html`, `evidence.html` และ `feedback.html` เมื่อมี feedback; ถ้าต้องการ Word ให้สร้างจาก Markdown ภายในชุดเดียวกันด้วย runtime ที่ฝัง

## Output contract

- `report.html`: รายงานหลัก UTF-8 เปิดด้วย browser ได้ทันที CSS ฝังในไฟล์หรืออยู่ในโฟลเดอร์ output
- `coverage.html`: ตาราง mapping ข้อกำหนดอาจารย์กับบท คำตอบ หลักฐาน Framework และสถานะ
- `evidence.html`: claim, status, source, date, scope และ limitation
- `feedback.html`: feedback, จุดที่แก้, ตำแหน่ง, หลักฐาน และวิธีตรวจ เมื่อมี feedback
- `report.docx`: สร้างเมื่อผู้ใช้ขอหรือโจทย์กำหนด โดยใช้ `vendor/thai-docx-upstream/scripts/thai_docx`

Markdown ใช้เป็น source ภายในเพื่อสร้าง HTML และ Word ไม่ใช่ output หลัก เว้นแต่ผู้ใช้ขอ

## Gates

- **Assignment Gate**: มี brief หรือขอบเขตที่ผู้ใช้ยืนยัน ถ้าไม่มีให้หยุดที่การรับโจทย์
- **Business Readiness Gate**: brief, หลักฐาน, ปัญหา, เป้าหมาย, constraints และ trade-offs พร้อม
- **Coverage Gate**: ข้อกำหนดบังคับทุกข้อมี answer, location, evidence หรือสถานะ limitation ที่ชัด
- **Feedback Gate**: feedback ที่ระบุว่าต้องแก้ถูกปิด และจุดแข็งที่ต้องรักษายังอยู่
- **Export Gate**: HTML เปิดได้; Word ต้องผ่าน build และ `check` พร้อมรายงาน warnings

ใช้ `python3 scripts/readiness_gate.py <workspace>/interview-state.json` และ `python3 scripts/coverage_gate.py <workspace>/coverage.json` ตัวตรวจ coverage ตรวจเฉพาะรายการที่ได้รับ ไม่ยืนยันความครบเทียบโจทย์ต้นฉบับหรือคุณภาพคำตอบ ผู้ช่วยต้องเทียบทั้งแปดข้อและ feedback ด้วย

## Framework rules

เลือกเครื่องมือจากโจทย์และข้อมูล เช่น BMC, Empathy Map, VPC, PESTEL, Five Forces, Benchmark, SWOT/TOWS, Materiality, Double Materiality, Value Chain, VRIO, SVAT, LCA Screening, McKinsey 7S, Roadmap, RACI, Skill Matrix, Logic Model, KPI, PDCA, GRI, SET, SDGs และ ACAT

แต่ละเครื่องมือต้องระบุว่าใช้เพื่อเปลี่ยนการตัดสินใจเรื่องใด หากไม่เกี่ยวข้องให้ระบุ `not_applicable` พร้อมเหตุผล ไม่สร้างคะแนน ผลสำรวจ baseline ROI หรือผลกระทบจากความว่างเปล่า

## Evidence rules

- `verified`: ผู้ช่วยตรวจแหล่งแล้ว
- `user_reported`: ผู้ใช้ให้ข้อมูล พร้อมบทบาทและช่วงเวลา
- `hypothesis`: สมมติฐานที่ต้องทดสอบ
- `proposed`: ข้อเสนอ เป้าหมาย หรือวิธีวัดใหม่
- `unknown`: ยังไม่มีข้อมูล

ตัวเลขต้องมี source, วันที่, หน่วย และขอบเขต ข้อมูลขัดกันต้องเก็บทั้งค่าและนิยาม ห้ามเลือกค่าที่ทำให้แผนดูดีขึ้นเงียบ ๆ

## Word export

เมื่อผู้ใช้ขอ Word:

1. ใช้ Markdown source ที่ผ่าน coverage และ verification แล้ว
2. เรียก `python3 scripts/build_outputs.py <source.md> <output-dir> --coverage <coverage.json> --evidence <evidence.json> --word` ตัวสร้าง HTML ใช้ Pandoc ถ้าไม่มี ให้ Agent เลือกเครื่องมือ HTML ที่มีหรือเขียน HTML จากเนื้อหาที่ตรวจแล้ว โดยคงลิงก์ ตาราง เชิงอรรถ และเนื้อหาครบ
3. อ่าน JSON และ exit code จากคำสั่ง
4. ถ้าสร้างสำเร็จ เรียก `check` กับไฟล์ใหม่
5. ส่งชื่อไฟล์ settings และ warnings ตามผลจริง

ใช้ runtime ที่ฝังก่อน ถ้าใช้ไม่ได้ ให้ Agent วินิจฉัยและเลือกเครื่องมือ Word อื่นที่ environment รองรับ เช่น Pandoc หรือ LibreOffice ได้ ไม่ต้องให้ผู้ใช้ติดตั้ง skill แยก ต้องตรวจข้อความ ตาราง ลิงก์ และภาษาไทยเทียบต้นฉบับ ใช้ bundled check เมื่อเรียกได้ และระบุข้อจำกัดที่ตรวจไม่ได้ ห้ามเปลี่ยนนามสกุล HTML เป็น DOCX หรืออ้างว่าสำเร็จโดยไม่มีไฟล์จริง

## Verification

ตรวจว่ารายงานตอบข้อกำหนดบังคับครบ หลักฐานตรงกับ claim ข้อเสนอไม่ถูกเขียนเป็นผลจริง ไม่มี placeholder ไม่มีข้อมูลกรณีตัวอย่างหลุด และ output ตรงกัน

รันชุดทดสอบ:

```text
python3 tests/test_readiness_gate.py
python3 tests/test_coverage_gate.py
```

การผ่าน unit tests ไม่เท่ากับการตรวจคุณภาพเนื้อหาหรือการเปิด Word ด้วยโปรแกรมจริง ต้องรายงานขอบเขตการตรวจตามที่ทำจริง

## Pitfalls

- อย่าเริ่มจาก Framework ก่อนอ่านโจทย์อาจารย์
- อย่าถามผู้ใช้ให้กรอกทุก Canvas เอง ให้ผู้ช่วยวิเคราะห์จากหลักฐาน
- อย่าใช้ชื่อบริษัท ตัวเลข กลยุทธ์ หรือคำตอบจากงานอื่นเป็นค่าเริ่มต้น
- อย่าใช้ Value Protection/Creation, LCA, GRI หรือ ACAT ถ้าไม่เกี่ยวข้องกับบริบทโดยไม่อธิบายเหตุผล
- อย่าฝังข้อมูลบริษัทผู้ใช้ไว้ใน Skill หรือ template กลาง
