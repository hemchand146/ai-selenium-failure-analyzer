# ai-selenium-failure-analyzer
Selenium automation framework with a post-execution AI failure analyzer that automatically reviews failed test logs and generates a consolidated debugging summary.

# 🧪 AI Selenium Automation Framework

## 📌 Overview
This repository contains a **sample Selenium test automation framework** created for learning, design exploration, and discussion.

It demonstrates common automation practices such as **Page Object Model (POM)**, **data-driven testing**, **structured logging**, and **post-execution reporting**.  
In addition, it includes a **separate AI-assisted post-failure analysis layer** that runs independently after test execution.

---

## ❓ Problem Statement
In Selenium automation frameworks, a test suite execution typically produces:
- ✅ One consolidated results file showing PASS / FAIL status  
- 📄 Multiple individual log files — one per test case  

In larger test suites (for example, dozens or hundreds of test cases), partial failures can result in many individual log files. Manually opening each log to understand failures becomes repetitive and time-consuming.

Re-running the entire test suite just to analyze failures is often unnecessary.

---

## 💡 Solution Approach
This framework introduces a **post-execution AI-assisted failure analysis layer**, designed as a **separate module**, fully decoupled from test execution.

### 🔄 How it works:
1. The test suite runs once and generates logs and a consolidated results file.
2. The analyzer reads the results file to identify **failed test cases only**.
3. Corresponding log files are processed.
4. A **single consolidated failure summary** is generated.

Because this analysis runs **after execution**, the test suite does **not need to be re-run**.  
Whenever failure analysis is required, the analyzer can be executed independently using existing logs.

---

## 🤖 AI Failure Analysis
The AI layer is intentionally **basic and exploratory**.

For each failed test case, it generates:
- 🧾 Failure reason  
- 🔍 Possible causes  
- 🧠 What to check first  
- 🛠 Suggested fixes  

The goal is to **reduce manual log inspection** and provide a faster starting point for debugging.  
The accuracy of insights depends on the **clarity and quality of execution logs**.

---

## ✨ Key Characteristics
- 🧪 Sample Selenium test automation framework  
- 📐 Page Object Model (POM) design  
- 📊 JSON-based test data  
- 🪵 Structured logging with screenshots on failure  
- ⏱ Post-execution analysis (no impact on test runtime)  
- 🤖 AI used only for failure summarization  
- 🔌 Clear separation between execution and analysis  

---

## 🗂 Project Structure
AI_Selenium/
├── Testcases/ # Test scripts
├── Pages/ # Page Object classes
├── TestData/ # JSON test data
├── AI/ # AI failure analysis modules
├── core/ # Base framework classes
├── utils/ # Utilities (logging, helpers)
├── Logs/ # Execution logs & screenshots
├── Reports/ # Test results & summaries
├── run.py # Test runner
└── README.md

---
⚠️ Notes
  AI analysis does not replace logs or manual debugging
  Raw execution logs remain the primary source of truth
  AI output should be treated as guided insight, not an exact root cause
  Quality of analysis depends on how clearly logs are written

🛠 Tech Stack
  🐍 Python
  🌐 Selenium WebDriver
  📐 Page Object Model (POM)
  📄 JSON-based configuration
  🤖 OpenAI-compatible LLM (via API)


## ▶️ Usage
## Run the test suite using a suite configuration file:
```bash
python run.py TestData/test_suite.json
```
You will get the automation_results.json    Which is the input for the Analyser.

## Run AI failure analysis (post-execution):
```bash
python -m AI.summarize_failures
```




