document.addEventListener('DOMContentLoaded', function () {
    const courseButtons = document.querySelectorAll('.course-btn');
   

    courseButtons.forEach(button => {
        button.addEventListener('click', function () {
            const courseName = button.getAttribute('data-coursename');
            const course = JSON.parse(button.getAttribute('data-course'));
            const instructors = JSON.parse(button.getAttribute('data-instructor'));
            toggleCourseCard(course , instructors , courseName );
        });
    });

    function toggleCourseCard(course , instructors , courseName) {
        const courseCard = document.querySelector(`.course-card[data-coursename="${courseName}"]`);

        if (courseCard) {
            courseCard.classList.toggle('d-none');
        } else {
            createCourseCard(course , instructors , courseName);
        }
       
    }

    function createCourseCard(course , instructors , courseName) {
        const courseCardsContainer = document.querySelector('.course-cards');
        const courseCard = document.createElement('div');
        courseCard.classList.add('card', 'mb-3', 'course-card');
        courseCard.setAttribute('data-coursename', courseName);

        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        const cardTitle = document.createElement('h5');
        cardTitle.classList.add('card-title');
        cardTitle.textContent = course[courseName].coursename + "("+ course[courseName].courseId+")";

        const creditHours = document.createElement('p');
        creditHours.classList.add('card-text');
        creditHours.textContent = `Credit Hours: ${course[courseName].creditHours}`;

        cardBody.appendChild(cardTitle);
        // Add instructor information
        if (Object.keys(instructors[courseName]).length > 0) {
            const instructorsList = document.createElement('ul');
            instructorsList.classList.add('list-group', 'list-group-flush');
            for (var i = 0; i < Object.keys(instructors[courseName]).length; i++) {
                const instructorItem = document.createElement('li');
                instructorItem.classList.add('list-group-item');
                instructorItem.textContent = `Instructor${i+1}: ${instructors[courseName][i].FirstName} ${instructors[courseName][i].LastName}`;            
                instructorsList.appendChild(instructorItem);
            }
            cardBody.appendChild(instructorsList);
        }
    

        courseCard.appendChild(cardBody);
        cardBody.appendChild(creditHours);

        courseCardsContainer.appendChild(courseCard);
    }
});