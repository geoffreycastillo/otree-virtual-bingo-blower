function saveAnswers(probabilities_length) {
    const otreeNextButton = document.querySelector('.otree-btn-next')

    // create the array holding all the answers
    let answers = Array(2 * probabilities_length);

    // get all buttons
    const labels = document.querySelectorAll('.choice-A-B-buttons label');

    const hiddenField = document.getElementById('hidden-choices')

    // fire when one of the button groups change
    labels.forEach((labelFirstLoop, indexFirstLoop) => {
        labelFirstLoop.addEventListener('click', (event) => {
            const letterChosen = labelFirstLoop.querySelector('input').value

            labels.forEach((labelSecondLoop, indexSecondLoop) => {
                const input = labelSecondLoop.querySelector('input')
                if (letterChosen === 'B') {
                    if ((indexSecondLoop < indexFirstLoop - 1 && input.value === 'A')
                        || (indexSecondLoop > indexFirstLoop && input.value === 'B')) {
                        $(labelSecondLoop).button('toggle');
                    }
                }
                if (letterChosen === 'A') {
                    if ((indexSecondLoop < indexFirstLoop && input.value === 'A')
                        || (indexSecondLoop > indexFirstLoop + 1 && input.value === 'B')) {
                        $(labelSecondLoop).button('toggle');
                    }
                }
            })
            otreeNextButton.disabled = false;
        })
    })

    otreeNextButton.addEventListener('click', () => {
        labels.forEach((label, index) => {
            if (label.classList.contains('active')) {
                answers[index] = label.querySelector('input').value
                answers = answers.filter(Boolean)
                hiddenField.value = answers
            }
        })
    })
}

