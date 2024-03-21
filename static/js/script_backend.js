$(document).ready(function() {
    // Fonction pour charger et afficher tous les feedbacks existants
    function loadFeedbacks() {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/feedback',
            type: 'GET',
            success: function(data) {
                $('#feedback-list').empty();
                data.forEach(function(feedback) {
                    $('#feedback-list').append(`
                        <li>
                            <strong>Nom du bootcamp:</strong> ${feedback.bootcampname}<br>
                            <strong>Priorité de retour:</strong> ${feedback.prioriteRetour}<br>
                            <strong>Type de retour:</strong> ${feedback.typeRetour}<br>
                            <strong>Évaluation:</strong> ${feedback.rating}<br>
                            <strong>Commentaires:</strong> ${feedback.comments}<br>
                            <button onclick="editFeedback('${feedback.unique_id}')">Modifier</button>
                            <button onclick="deleteFeedback('${feedback.unique_id}')">Supprimer</button>
                        </li>
                    `);
                });
            }
        });
    }

    // Charger et afficher les feedbacks lors du chargement de la page
    loadFeedbacks();

    // Fonction pour supprimer un feedback
    window.deleteFeedback = function(unique_id) {
        if (confirm("Voulez-vous vraiment supprimer ce feedback ?")) {
            $.ajax({
                url: 'http://127.0.0.1:5000/api/feedback/' + unique_id,
                type: 'DELETE',
                success: function() {
                    loadFeedbacks(); // Recharger la liste des feedbacks après la suppression
                }
            });
        }
    }

    // Fonction pour éditer un feedback
    window.editFeedback = function(unique_id) {
        // Récupérer le feedback à modifier en faisant une requête GET au serveur
        $.ajax({
            url: 'http://127.0.0.1:5000/api/feedback/' + unique_id,
            type: 'GET',
            success: function(feedback) {
                // Afficher un formulaire pré-rempli avec les données du feedback
                var form = `
                    <form id="edit-feedback-form">
                        <div class="form-group">
                            <label for="bootcampname">Nom du bootcamp :</label>
                            <input type="text" id="bootcampname" name="bootcampname" value="${feedback.bootcampname}" required>
                        </div>
                        <div class="form-group">
                            <label for="prioriteRetour">Priorité de retour :</label>
                            <input type="text" id="prioriteRetour" name="prioriteRetour" value="${feedback.prioriteRetour}" required>
                        </div>
                        <div class="form-group">
                            <label for="typeRetour">Type de retour :</label>
                            <input type="text" id="typeRetour" name="typeRetour" value="${feedback.typeRetour}" required>
                        </div>
                        <div class="form-group">
                            <label for="rating">Évaluation :</label>
                            <input type="number" id="rating" name="rating" min="1" max="5" value="${feedback.rating}" required>
                        </div>
                        <div class="form-group">
                            <label for="comments">Commentaires :</label>
                            <textarea id="comments" name="comments" rows="4" required>${feedback.comments}</textarea>
                        </div>
                        <button type="submit">Enregistrer</button>
                    </form>
                `;
                
                // Remplacer le contenu de la page par le formulaire d'édition
                $('.container').html(form);
                
                // Lorsque le formulaire est soumis, envoyer une requête PATCH pour mettre à jour le feedback
                $('#edit-feedback-form').submit(function(event) {
                    event.preventDefault();
                    
                    var formData = {
                        bootcampname: $('#bootcampname').val(),
                        prioriteRetour: $('#prioriteRetour').val(),
                        typeRetour: $('#typeRetour').val(),
                        rating: $('#rating').val(),
                        comments: $('#comments').val()
                    };
                    
                    $.ajax({
                        url: 'http://127.0.0.1:5000/api/feedback/' + unique_id,
                        type: 'GET',//'PATCH',
                        contentType: 'application/json',
                        data: JSON.stringify(formData),
                        success: function(response) {
                            alert('Feedback mis à jour avec succès');
                            // Recharger la page pour afficher les modifications
                            window.location.reload();
                        },
                        error: function(xhr, status, error) {
                            alert('Erreur lors de la mise à jour du feedback');
                            console.error(xhr.responseText);
                        }
                    });
                });
            }
        });
    }

});
