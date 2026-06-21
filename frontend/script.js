async function predictRisk() {

    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "Analyzing...";

    const payload = {

        Age: parseInt(
            document.getElementById("Age").value
        ),

        RestingBP: parseFloat(
            document.getElementById("RestingBP").value
        ),

        Cholesterol: parseFloat(
            document.getElementById("Cholesterol").value
        ),

        FastingBS: parseInt(
            document.getElementById("FastingBS").value
        ),

        MaxHR: parseFloat(
            document.getElementById("MaxHR").value
        ),

        Oldpeak: parseFloat(
            document.getElementById("Oldpeak").value
        ),

        Sex: document.getElementById("Sex").value,

        ChestPainType:
            document.getElementById("ChestPainType").value,

        RestingECG:
            document.getElementById("RestingECG").value,

        ExerciseAngina:
            document.getElementById("ExerciseAngina").value,

        ST_Slope:
            document.getElementById("ST_Slope").value
    };

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        if (!data.success) {

            resultDiv.innerHTML = `
                <div class="result-danger">
                    Prediction Failed
                </div>
            `;

            return;
        }

        if (data.prediction === 1) {

            resultDiv.innerHTML = `
                <div class="result-danger">
                    <h2>🔴 HIGH RISK</h2>

                    <div class="confidence">
                        Confidence:
                        ${data.confidence}%
                    </div>
                </div>
            `;
        }

        else {

            resultDiv.innerHTML = `
                <div class="result-success">
                    <h2>🟢 LOW RISK</h2>

                    <div class="confidence">
                        Confidence:
                        ${data.confidence}%
                    </div>
                </div>
            `;
        }

    }

    catch (error) {

        console.error(error);

        resultDiv.innerHTML = `
            <div class="result-danger">
                Could not connect to API
            </div>
        `;
    }
}