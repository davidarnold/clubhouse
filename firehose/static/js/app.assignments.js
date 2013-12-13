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
    var task_claim_selector = '[data-type="task"] button[data-action="claim"]',
        assignment_checkbox_selector = '[data-type="assignment"] input[type="checkbox"]',
        assignment_release_selector = '[data-type="assignment"] button[data-action="release"]',
        $assignment_note_modal = $('#assignment-note-modal'),
        $assignment_note_submit = $assignment_note_modal.find('[data-action="submit"]'),
        $assignment_note_cancel = $assignment_note_modal.find('[data-action="cancel"]');

    $(document).on('click', task_claim_selector, function () {
        var $button = $(this),
            $task = $button.closest('[data-type="task"]'),
            task_id = $task.data('taskId');

        $.ajax({
            url: window.IMPLEMENTATION_TASK_CLAIM_URL,
            type: 'POST',
            data: {
                task_id: task_id,
            },
            dataType: 'html',
            success: function (data) {
                $task.replaceWith(data);
            },
            error: function (data) {
                window.alert('Well this is embarrassing.  Something went wrong.')
            }
        });
    });

    $(document).on('change', assignment_checkbox_selector, function () {
        var $checkbox = $(this),
            $assignment = $checkbox.closest('[data-type="assignment"]'),
            assignment_id = $assignment.data('assignmentId');

        $.ajax({
            url: window.IMPLEMENTATION_ASSIGNMENT_CHECKED_URL,
            type: 'POST',
            data: {
                assignment_id: assignment_id,
                checked: $checkbox.prop('checked')
            },
            dataType: 'html',
            success: function (data) {
                $assignment.replaceWith(data);
            },
            error: function (data) {
                window.alert('Well this is embarrassing.  Something went wrong.')
            }
        });
    });

    $(document).on('click', assignment_release_selector, function () {
        var $button = $(this),
            $assignment = $button.closest('[data-type="assignment"]'),
            assignment_id = $assignment.data('assignmentId');

        $.ajax({
            url: window.IMPLEMENTATION_ASSIGNMENT_RELEASE_URL,
            type: 'POST',
            data: {
                assignment_id: assignment_id,
            },
            dataType: 'html',
            success: function (data) {
                $assignment.replaceWith(data);
            },
            error: function (data) {
                window.alert('Well this is embarrassing.  Something went wrong.')
            }
        });
    });

    $assignment_note_modal.on('hidden', function() {
        // Force form to be reloaded
        $(this).removeData('modal');
        $(this).find('.modal-body').text('Loading ...');
    }).on('shown', function() {
        $(this).find('#id_note').focus();
    });

    $assignment_note_cancel.click(function (e) {
        $assignment_note_modal.modal('hide');
        e.preventDefault();
    });

    $assignment_note_submit.click(function (e) {
        var $form = $assignment_note_modal.find('form[data-type="assignment-note"]'),
            assignment_id = $form.data('assignmentId'),
            $assignment_note_modal_body = $assignment_note_modal.find('.modal-body'),
            $assignment = $('[data-type="assignment"][data-assignment-id="' + assignment_id + '"]');

        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: $form.serialize(),
            dataType: 'html',
            success: function (data) {
                $assignment.replaceWith(data);
                $assignment_note_modal.modal('hide');
            },
            error: function (data) {
                $assignment_note_modal_body.html(data.responseText);
            }
        });

        e.preventDefault();
    });
});