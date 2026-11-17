# Thai Strategy to Word

Skill สำหรับพัฒนารายงานจากโจทย์อาจารย์ ข้อมูลบริษัท หลักฐานสาธารณะ และ feedback ใช้ได้กับทุกอุตสาหกรรม ไม่ผูกกับบริษัท วิชา หรือตำแหน่งงานใด

## เริ่มใช้งานครั้งแรก

เริ่มด้วยข้อความนี้:

> ใช้ thai-strategy-to-word ช่วยทำรายงานตามคำถามแปดข้อและ feedback ที่อยู่ใน Skill เริ่มถามบริษัทและงานของฉันทีละขั้น

Skill มีคำถามแปดข้อและ feedback ฉบับไม่ผูกบริษัทไว้ใน `references/course-requirements.md` แล้ว ไม่ต้องส่งใหม่ เริ่มจากคำถามว่าคุณทำงานที่ไหน บริษัททำธุรกิจอะไร และรับผิดชอบส่วนใด

ถ้ามีคำสั่งใหม่ เกณฑ์คะแนน หรือ feedback เพิ่ม ส่งเป็นข้อความ รูป หรือไฟล์ได้ “รับโจทย์อาจารย์” หมายถึงอ่านข้อกำหนดเหล่านี้ ไม่ใช่ให้ผู้ใช้คิดโจทย์หรือกรอก Framework เอง

Skill จะทำตามลำดับนี้:

```text
ถามบริษัทและบทบาทผู้ใช้
→ ใช้คำถามแปดข้อและ feedback ที่ฝังไว้ พร้อมคำสั่งเพิ่มเติมถ้ามี
→ ข้อมูลบริษัทและปัญหา
→ ค้นหลักฐานสาธารณะ
→ รับข้อมูลภายใน
→ Coverage Plan
→ วิเคราะห์ Framework
→ เขียนรายงาน
→ ตรวจความครบและหลักฐาน
→ report.html
→ report.docx เมื่อขอ
```

ถ้ายังไม่เข้าใจโจทย์อาจารย์ ให้ส่งข้อความสั้น ๆ ว่า:

> ฉันยังไม่เข้าใจว่าโจทย์อาจารย์ต้องการอะไร ช่วยอ่านเอกสารที่ให้ แล้วแปลเป็นรายการสิ่งที่ต้องส่ง คำถามที่ต้องตอบ Framework ที่ต้องใช้ และเกณฑ์ตรวจงาน

Skill จะไม่เติมข้อกำหนดที่ไม่มีใน brief และจะแยก `required`, `conditional`, `optional` กับ `unknown` ให้เห็น

## Output

Output หลักเป็น HTML เปิดด้วย browser ได้ทันที:

- `report.html` รายงานฉบับหลัก
- `coverage.html` ตารางตรวจว่าตอบโจทย์อาจารย์ครบหรือไม่
- `evidence.html` ทะเบียนหลักฐาน แหล่งที่มา วันที่ ขอบเขต และข้อจำกัด
- `feedback.html` ตารางว่าแก้ feedback ข้อใดไว้ที่ไหน เมื่อมี feedback

Markdown เป็น source ภายในเพื่อสร้าง HTML และ Word ไม่ใช่ output หลัก

## Word

ฝัง `thai-docx` v0.3.4 ไว้ใน `vendor/thai-docx-upstream/` แล้ว ไม่ต้องติดตั้งแยก

เมื่อผู้ใช้ขอ Word Skill จะ:

1. ใช้ source ที่ผ่าน readiness, coverage และ verification แล้ว
2. สร้าง `.docx` ด้วย runtime ที่ฝังไว้
3. อ่าน exit code และ JSON result
4. รัน `check` กับไฟล์ที่สร้าง
5. รายงานชื่อไฟล์ ฟอนต์ ขนาด กระดาษ warnings และขอบเขตการตรวจ

ตัว runtime ไม่มี package ภายนอก ต้องใช้ Python 3.11+ หรือ Node.js 22+

## สร้าง output ทั้งชุด

```text
python3 scripts/build_outputs.py report.md output/ --coverage coverage.json --evidence evidence.json --word
```

ตัด `--word` ถ้าต้องการ HTML อย่างเดียว

ตัวสร้าง HTML ใช้ Pandoc ที่ติดตั้งใน environment (ไม่ได้ฝังในชุดนี้) ถ้าไม่มี Agent เลือกเครื่องมืออื่นหรือเขียน HTML จากเนื้อหาที่ตรวจแล้วได้ ส่วน Word ใช้ runtime ที่ฝังก่อน หากล้มเหลว Agent เลือกวิธีสำรองเองและตรวจไฟล์จริง ไม่ต้องติดตั้ง skill แยก

## License

โค้ดของ Skill นี้อยู่ภายใต้ license ของ repository นี้ ส่วน Thai DOCX ที่ฝังมาจาก:

- upstream: https://github.com/sayam/thai-docx-skill
- version: 0.3.4
- license: MIT, Copyright (c) 2026 Sayam Sriphua

รายละเอียดและ license ของส่วนประกอบอยู่ใน [vendor/THIRD_PARTY.md](vendor/THIRD_PARTY.md) และ `vendor/thai-docx-upstream/LICENSES/`

## ไฟล์สำคัญ

- `SKILL.md`: workflow หลัก
- `workflows/first-run.md`: ขั้นตอนสำหรับผู้ใช้ครั้งแรก
- `references/`: หลักฐาน Framework การสัมภาษณ์ และการตรวจงาน
- `templates/assignment-profile.example.json`: โครงรับโจทย์อาจารย์
- `templates/coverage.example.json`: โครงตรวจ coverage
- `scripts/readiness_gate.py`: ตรวจความพร้อมของโจทย์และข้อมูล
- `scripts/coverage_gate.py`: ตรวจความครบของคำถามอาจารย์
- `scripts/build_html.py`: สร้าง HTML standalone
- `scripts/export_word.py`: เรียก Thai DOCX ที่ฝังไว้
- `tests/`: unit tests และ conversation scenarios

## ตรวจระบบ

```text
python3 tests/test_readiness_gate.py
python3 tests/test_coverage_gate.py
```
