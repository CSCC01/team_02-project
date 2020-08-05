/**
 * Show the card associated by the given goal position.
 *
 * @param {number} i The goal position
 */
function show(i) {
    $('.card')
        .eq(i)
        .slideDown(1000, function () {
            $('.selected').removeClass('selected');
            $('.horizontal').removeClass('horizontal');
            $('.vertical').removeClass('vertical');
            $('.d-diagonal').removeClass('d-diagonal');
            $('.a-diagonal').removeClass('a-diagonal');
            $(`.r${parseInt(i / 5)}`).addClass('horizontal');
            $(`.c${i % 5}`).addClass('vertical');
            if (i % 5 === parseInt(i / 5)) $(`.d0`).addClass('d-diagonal');
            if (parseInt(i / 5) === 4 - (i % 5))
                $(`.d1`).addClass('a-diagonal');
            $('#board td').eq(i).addClass('selected');
            animationLock = false;
            $('#hint').hide();
        });
}

let animationLock = false; // Ensure synchronous card-swaps

/**
 * Add event listeners to each goal box so that their card shows and the previous card is hidden.
 */
for (let i = 0; i < $('.card').length; i++) {
    $('#board td')
        .eq(i)
        .click(function () {
            if (!animationLock) {
                animationLock = true;
                if ($('.card:visible').length !== 1) show(i);
                else $('.card:visible').slideUp(1000, () => show(i));
                $('#board td').eq(i).addClass('selected');
            }
        });
}

/**
 * Show the goal row associated by the given reward.
 */
function showGoal(j, reward) {
    $(reward)
        .eq(j)
        .slideDown(1000);
}

// let horRewAnimationLock = false;

/**
 * Add event listeners to each reward row so that their card shows.
 */
for (let j = 0; j < $('.card').length; j++) {
    $('#horizontal-reward')
        .eq(j)
        .click(function () {
            console.log("I was clicked"); // This doesn't show on log.
            //if (!horRewAnimationLock) {
                //horRewAnimationLock = true;
                if ($('.reward-card:visible').length !== 1) showGoal(j, '#horizontal-rc');
                else $('.reward-card:visible').slideUp(1000, () => showGoal('#horizontal-rc'));
            //}
        });
}

/*
function toggle(e) {
    if (!e) var e = window.event;                // Get the window event
    e.cancelBubble = true;                       // IE Stop propagation
    if (e.stopPropagation) e.stopPropagation();  // Other Broswers

    if( document.getElementById("horizontal-rc").style.display=='none' ){
       console.log(document.getElementById("horizontal-rc").style.display);
       document.getElementById("horizontal-rc").style.display = '';// set to table-row instead of an empty string
       console.log(document.getElementById("horizontal-rc").style.display);
    } else {
       document.getElementById("horizontal-rc").style.display = 'none';
    }
}*/