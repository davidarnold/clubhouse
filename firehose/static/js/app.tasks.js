/*
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License (the "License").
 * You may not use this file except in compliance with the License.
 *
 * You can obtain a copy of the License in the included LICENSE.txt
 * or http://opensource.org/licenses/CDDL-1.0
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When modifying Covered Code, update the affected files' copyright
 * notice with the current year and add your name to its contributors
 * list.
 *
 * Copyright 2012-2013 Clubhouse Contributors
 *
 * File contributors: David Arnold
 */
$(document).ready(function () {
    var $task_modal = $('#task-modal'),
        $task_submit = $task_modal.find('[data-action="submit"]'),
        $task_cancel = $task_modal.find('[data-action="cancel"]');

    $task_modal.on('hidden', function() {
        // Force form to be reloaded
        $(this).removeData('modal');
        $(this).find('.modal-body').text('Loading ...');
    }).on('shown', function() {
        $(this).find('#id_description').focus();
    });

    $task_cancel.click(function (e) {
        $task_modal.modal('hide');
        e.preventDefault();
    });

    $task_submit.click(function (e) {
        var $form = $task_modal.find('form[data-type="task"]'),
            $deliverable_field = $form.find('#id_deliverable'),
            $task_modal_body = $task_modal.find('.modal-body'),
            $tasks = $('[data-type="tasks"][data-deliverable-id="' + $deliverable_field.val() + '"]');

        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: $form.serialize(),
            dataType: 'html',
            success: function (data) {
                $tasks.show();
                $tasks.append(data);
                $task_modal.modal('hide');
            },
            error: function (data) {
                $task_modal_body.html(data.responseText);
            }
        });

        e.preventDefault();
    });
});
