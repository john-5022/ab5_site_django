const $startDateDeadline = $('#start-date-deadline'), $endDateDeadline = $('#end-date-deadline');
const $startDateReview = $('#start-date-review'), $endDateReview = $('#end-date-review');
const $deadlineDateError = $('#deadline-date-error'), $reviewDateError = $('#review-date-error')
let selectedTaskState = null;
const $taskFilterForm = $('#task-filters-form');

$('#task-state').change(function() {
    selectedTaskState = parseInt($(this).val());
});

const createDate = dateStr => {
    const parts = dateStr.split("/");
    const day = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1; // Months are 0-indexed, so subtract 1
    const year = parseInt(parts[2], 10);

    return new Date(year, month, day);
}

const validateBeforeAfterDates = (before, after) => {
    const beforeDate = createDate(before.val());
    const afterDate = createDate(after.val());
    if (afterDate <= beforeDate){
        throw new Error('Start date should be before end date');
    }
}

const showError = (errorDiv, errorMsg) => {
    errorDiv.text(errorMsg);
    errorDiv.show();
}

const validateData = () => {
    try{
        validateBeforeAfterDates($startDateDeadline, $endDateDeadline);
    } catch (e) {
        showError($deadlineDateError, e)
        return false
    }
    try{
        validateBeforeAfterDates($startDateReview, $endDateReview);
    } catch (e) {
        showError($reviewDateError, e)
        return false
    }
    return true
}

function handleIconClick(element){
    const $element = $(element).parent().find('input:first');
    $element.click();
}

const hideErrors = () => {
    $deadlineDateError.hide()
    $reviewDateError.hide()
}

$('#clear-dates-deadline').click(function(event) {
    event.preventDefault();
    $startDateDeadline.val(null);
    $endDateDeadline.val(null);
});

$('#clear-dates-review').click(function(event) {
    event.preventDefault();
    $startDateReview.val(null);
    $endDateReview.val(null);
});
