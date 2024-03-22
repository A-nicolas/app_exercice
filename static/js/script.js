document.getElementById('date_feedback').value = new Date().toLocaleString("fr");
document.getElementById('date_feedback_affichage').value = new Date().toLocaleDateString("fr");
const value = document.querySelector("#ratingvalue");
const input = document.querySelector("#rating");
value.textContent = input.value;
input.addEventListener("input", (event) => {
  value.textContent = event.target.value;
});

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('feedback-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Empêcher le formulaire de se soumettre normalement

        const formData = new FormData(form);
        formData.set("consentement", document.getElementById("consentement").checked);

        const jsonData = {};

        // Convertir les données du formulaire en JSON
        formData.forEach(function(value, key){
            jsonData[key] = value;
        });

        // Envoyer les données JSON à un script Python
        fetch('http://127.0.0.1:5000/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de l\'envoi des données');
            }
            alert("Données envoyées avec succès au script python")
            console.log('Données envoyées avec succès au script python');
        })
        .catch(error => console.error('Erreur:', error));
    });
});

function setAttachedFileName(input) {
    const fileNameField = document.getElementById('attachedfiles');
    if (input.files.length > 0) {
        const fileName = input.files[0].name;
        fileNameField.value = fileName;
    }
}
