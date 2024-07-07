document
  .getElementById("search-button")
  .addEventListener("click", async function () {
    const query = document.getElementById("search-input").value;
    if (!query) {
      alert("검색어를 입력해주세요.");
      return;
    }

    const response = await fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        query: query,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      document.getElementById("report-title").innerText = data.report_title;
      document.getElementById("main-text").innerText = data.main_text;
      document.getElementById("relate").innerText = data.relate;
      const oracleList = document.getElementById("oracle");
      oracleList.innerHTML = ""; // Clear previous results
      data.oracle.forEach((item) => {
        const li = document.createElement("li");
        li.innerText = item;
        oracleList.appendChild(li);
      });
    } else {
      alert("보고서를 생성하는 데 문제가 발생했습니다.");
    }
  });
