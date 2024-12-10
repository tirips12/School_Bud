document.addEventListener('DOMContentLoaded', function() {
    const voteButtons = document.querySelectorAll('.vote-button');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    voteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const container = this.closest('.vote-container');
            const contentType = container.dataset.type;
            const objectId = container.dataset.id;
            const voteType = this.dataset.vote === 'up' ? 'UP' : 'DOWN';
            
            fetch('/vote/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `content_type=${contentType}&object_id=${objectId}&vote_type=${voteType}`
            })
            .then(response => {
                if (response.status === 403) {
                    window.location.href = '/login/';
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (data && data.status === 'success') {
                    const voteCount = container.querySelector('.vote-count');
                    voteCount.textContent = data.new_vote_count;
                    
                    const reputationElement = document.querySelector('.user-reputation');
                    if (reputationElement) {
                        reputationElement.textContent = data.new_reputation;
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
