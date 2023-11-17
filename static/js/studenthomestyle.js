
    document.addEventListener('DOMContentLoaded', function () {
        // Get all course buttons
        const courseButtons = document.querySelectorAll('.course-btn');

        // Add click event listener to each course button
        courseButtons.forEach(button => {
            button.addEventListener('click', function () {
                const courseName = button.getAttribute('data-course');
                toggleCourseCard(courseName);
            });
        });

        // Function to toggle course information card
        function toggleCourseCard(courseName) {
            const courseCard = document.querySelector(`.course-card[data-course="${courseName}"]`);

            if (courseCard) {
                // If the card exists, toggle its visibility
                courseCard.classList.toggle('d-none');
            } else {
                // If the card doesn't exist, create and append it
                createCourseCard(courseName);
            }
        }

        // Function to create a course information card
        function createCourseCard(courseName) {
            const courseCardsContainer = document.querySelector('.course-cards');

            const courseCard = document.createElement('div');
            courseCard.classList.add('card', 'mb-3', 'course-card');
            courseCard.setAttribute('data-course', courseName);

            const cardBody = document.createElement('div');
            cardBody.classList.add('card-body');

            const cardTitle = document.createElement('h5');
            cardTitle.classList.add('card-title');
            cardTitle.textContent = courseName;

            const cardText = document.createElement('p');
            cardText.classList.add('card-text');
            // Add content for the course card

            cardBody.appendChild(cardTitle);
            cardBody.appendChild(cardText);
            courseCard.appendChild(cardBody);

            courseCardsContainer.appendChild(courseCard);
        }
    });
