$('.toggle-hide-icon').on('click', event => {
    const element = $(event.target);
    const parent = element.parent().parent();
    parent.find('.hide-able').toggleClass('hidden');
    element.toggleClass('bi-caret-down');
    element.toggleClass('bi-caret-up');
})
