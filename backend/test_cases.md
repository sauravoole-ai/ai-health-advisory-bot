This file lists the scenarios that were actually tested during development of the **AI Health Advisory Assistant**.

---

## ✅ Test Summary

| TC No. | Feature | Test Scenario | Status |
|---|---|---|---|
| TC-01 | Backend | Health check API opened successfully | ✅ Tested |
| TC-02 | Manual Vitals | Normal reading: SpO₂ 97, BPM 78, mild tiredness | ✅ Tested |
| TC-03 | Manual Vitals | Caution reading: SpO₂ 93, BPM 88, weakness | ✅ Tested |
| TC-04 | Manual Vitals | Emergency reading: SpO₂ 88, BPM 82, severe breathlessness | ✅ Tested |
| TC-05 | Validation | Missing SpO₂ input returned validation error | ✅ Tested |
| TC-06 | AI Chatbot | General query: “I feel weak and tired. What should I do?” | ✅ Tested |
| TC-07 | AI Chatbot | Emergency query: “I have chest pain and severe breathlessness” | ✅ Tested |
| TC-08 | AI Chatbot | Multi-turn follow-up with symptom duration | ✅ Tested |
| TC-09 | AI Chatbot | Out-of-scope query: “What is 4+5?” | ✅ Tested |
| TC-10 | AI Chatbot | Identity query: “Who are you?” | ✅ Tested |
| TC-11 | AI Chatbot | Numeric ambiguity query: “30” | ✅ Tested |
| TC-12 | Browser UI | Manual vitals form worked in browser | ✅ Tested |
| TC-13 | Browser UI | AI chatbot worked in browser | ✅ Tested |
| TC-14 | Browser UI | Copy buttons worked | ✅ Tested |
| TC-15 | Browser UI | Clear buttons worked | ✅ Tested |
| TC-16 | Browser UI | Save as PDF / print window opened | ✅ Tested |
| TC-17 | Browser UI | Basic responsive layout checked | ✅ Basic Check Done |
