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
    var issue_checkbox_selector = '[data-type="issue"] input[type="checkbox"]',
        issue_button_selector = '[data-type="issue"] button[data-action]',
        $issue_modal = $('#issue-modal'),
        issue_priority_selector = '[name="priority"]',
        issue_assignee_selector = '[name="assignee"]',
        $issue_submit = $issue_modal.find('[data-action="submit"]'),
        $issue_cancel = $issue_modal.find('[data-action="cancel"]'),
        $issue_comment_modal = $('#issue-comment-modal'),
        $issue_comment_submit = $issue_comment_modal.find('[data-action="submit"]'),
        $issue_comment_cancel = $issue_comment_modal.find('[data-action="cancel"]');

    $(document).on('change', issue_checkbox_selector, function () {
        var $checkbox = $(this),
            $issue = $checkbox.closest('[data-type="issue"]'),
            issue_id = $issue.data('issueId');

        $.ajax({
            url: window.IMPLEMENTATION_ISSUE_CHECKED_URL,
            type: 'POST',
            data: {
                issue_id: issue_id,
                checked: $checkbox.prop('checked')
            },
            dataType: 'html',
            success: function (data) {
                $issue.replaceWith(data);
            },
            error: function (data) {
                window.alert('Well this is embarrassing.  Something went wrong.')
            }
        });
    });

    $(document).on('click', issue_button_selector, function () {
        var $button = $(this),
            $issue = $button.closest('[data-type="issue"]'),
            issue_id = $issue.data('issueId');

        $.ajax({
            url: window.IMPLEMENTATION_ISSUE_ACTION_URL,
            type: 'POST',
            data: {
                issue_id: issue_id,
                action: $button.data('action')
            },
            dataType: 'html',
            success: function (data) {
                $issue.replaceWith(data);
            },
            error: function (data) {
                window.alert('Well this is embarrassing.  Something went wrong.')
            }
        });
    });

    $issue_modal.on('hidden', function() {
        // Force form to be reloaded
        $(this).removeData('modal');
        $(this).find('.modal-body').text('Loading ...');
        $(this).find('.modal-footer a').removeAttr('disabled');
    }).on('shown', function() {
        $(this).find('#id_description').focus();
    });

    var fix_visibility = function (instant) {
        var $issue_priority = $issue_modal.find(issue_priority_selector),
            $issue_assignee = $issue_modal.find(issue_assignee_selector);

        if ($issue_priority.val() !== '30' /* Information */) {
            if (instant === true) {
                $issue_assignee.closest('.control-group').show();
            } else {
                $issue_assignee.closest('.control-group').slideDown();
            }
        } else {
            if (instant === true) {
                $issue_assignee.val('').closest('.control-group').hide();
            } else {
                $issue_assignee.val('').closest('.control-group').slideUp();
            }
        }
    };

    $(document).on('change', issue_priority_selector, fix_visibility);

    $issue_cancel.click(function (e) {
        $issue_modal.modal('hide');
        e.preventDefault();
    });

    $issue_submit.click(function (e) {
        var $this = $(this),
            $form = $issue_modal.find('form[data-type="issue"]'),
            $deliverable_field = $form.find('#id_deliverable'),
            $issue_modal_body = $issue_modal.find('.modal-body'),
            $issues = $('[data-type="issues"][data-deliverable-id="' + $deliverable_field.val() + '"]');

        if (!$this.attr('disabled')) {
            $this.attr('disabled', 'disabled');
            $.ajax({
                url: $form.attr('action'),
                type: $form.attr('method'),
                data: $form.serialize(),
                dataType: 'html',
                success: function (data) {
                    $issues.show();
                    $issues.append(data);
                    $issue_modal.modal('hide');
                },
                error: function (data) {
                    $issue_modal_body.html(data.responseText);
                    $this.removeAttr('disabled');
                    fix_visibility(true);
                }
            });
        }

        e.preventDefault();
    });

    $issue_comment_modal.on('hidden', function() {
        // Force form to be reloaded
        $(this).removeData('modal');
        $(this).find('.modal-body').text('Loading ...');
        $(this).find('.modal-footer a').removeAttr('disabled');
    }).on('shown', function() {
        $(this).find('#id_body').focus();
    });

    $issue_comment_cancel.click(function (e) {
        $issue_comment_modal.modal('hide');
        e.preventDefault();
    });

    $issue_comment_submit.click(function (e) {
        var $this = $(this),
            $form = $issue_comment_modal.find('form[data-type="issue-comment"]'),
            $issue_field = $form.find('#id_issue'),
            $issue_comment_modal_body = $issue_comment_modal.find('.modal-body'),
            $issue = $('[data-type="issue"][data-issue-id="' + $issue_field.val() + '"]');

        if (!$this.attr('disabled')) {
            $this.attr('disabled', 'disabled');
            $.ajax({
                url: $form.attr('action'),
                type: $form.attr('method'),
                data: $form.serialize(),
                dataType: 'html',
                success: function (data) {
                    $issue.replaceWith(data);
                    $issue_comment_modal.modal('hide');
                },
                error: function (data) {
                    $issue_comment_modal_body.html(data.responseText);
                }
            });
        }

        e.preventDefault();
    });
});
