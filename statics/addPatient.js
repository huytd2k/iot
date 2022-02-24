const createPatient = async () => {
    formData = $("#add_patient_form").serializeArray()
    body = {
        device_id: formData[0]["value"],
        doctor_email: formData[1]["value"],
        heartrate_threshhold: parseInt(formData[2]["value"]),
    }
    console.log(JSON.stringify(body))
    res = await fetch("/api/patient", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
    console.log(res.json())
}
