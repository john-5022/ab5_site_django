const $markDoneBtn = $('#mark-done-btn');
const $actionCheckBoxes = $('.action-checkbox');
let selectedIds = [];

const setChecked = () => {
    selectedIds = []
    $('.action-checkbox:checked').each((index, item) => {
        selectedIds.push($(item).data('id'));
    })
    $markDoneBtn.attr('disabled', !Boolean(selectedIds.length))
}

$actionCheckBoxes.on('click', () => {
    setChecked();
})

$('#show-completed-actions').on('change', () => {
    $('[data-isCompleted="0"]').toggleClass('hidden');
})

$('#check-all').change(function() {
    $actionCheckBoxes.prop('checked', this.checked);
    setChecked();
})

const getCookie = name => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
