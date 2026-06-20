"""Tests for host adapters and verification seams."""

from __future__ import annotations

import marimo as mo

from marimo_utils.ui.core.component import (
    DATA_COMPONENT,
    MarkupComponent,
    data_props_attr,
    format_data_attrs,
    verification_attrs,
)
from marimo_utils.ui.host import plain_html_page, setup_host, show
from marimo_utils.ui.host.tw_ready import DATA_TW_READY, TW_SENTINEL_ID
from marimo_utils.ui.host.verification import selectors_for_dump
from marimo_utils.ui.setup.bootstrap import bootstrap_tailwind


def test_verification_attrs_emits_data_component() -> None:
    attrs = verification_attrs(component="dr-hello", name="Ada")
    assert attrs[DATA_COMPONENT] == "dr-hello"
    assert attrs["name"] == "Ada"
    rendered = format_data_attrs(attrs)
    assert 'data-component="dr-hello"' in rendered
    assert 'name="Ada"' in rendered


def test_data_props_attr_is_compact_json() -> None:
    assert data_props_attr({"title": "Demo", "items": [1, 2]}) == (
        '{"title":"Demo","items":[1,2]}'
    )


def test_markup_component_injects_data_component_on_opening_tag() -> None:
    component = MarkupComponent(
        html='<dr-hello name="Ada"></dr-hello>',
        component="dr-hello",
    )
    assert 'data-component="dr-hello"' in component.to_html()


def test_markup_component_injects_on_root_when_nested_child_has_same_marker() -> None:
    component = MarkupComponent(
        html=(
            '<div class="wrap">'
            '<span data-component="dr-hello">nested</span>'
            "</div>"
        ),
        component="dr-hello",
    )
    rendered = component.to_html()
    assert rendered.startswith('<div class="wrap" data-component="dr-hello">')


def test_show_wraps_markup_in_mo_html_with_dr_scope() -> None:
    rendered = show('<dr-hello name="Ada"></dr-hello>')
    assert isinstance(rendered, mo.Html)
    assert rendered.text == (
        '<div class="dr-scope"><dr-hello name="Ada"></dr-hello></div>'
    )

    rendered_component = show(MarkupComponent(html="<span>ok</span>"))
    assert rendered_component.text == '<div class="dr-scope"><span>ok</span></div>'


def test_setup_host_returns_runtime_and_styles() -> None:
    runtime, styles = setup_host()
    runtime_html = str(runtime)
    styles_html = str(styles)
    assert "__drRuntimeLoaded" in runtime_html or "drRuntime" in runtime_html
    assert "dr-styles" in styles_html
    assert TW_SENTINEL_ID in styles_html
    assert "twReady" in styles_html


def test_plain_html_page_includes_scope_runtime_and_sentinel() -> None:
    page = plain_html_page(
        MarkupComponent(
            html='<dr-hello name="Ada"></dr-hello>',
            component="dr-hello",
        ),
        title="probe",
        include_runtime=False,
    )
    assert "<!DOCTYPE html>" in page
    assert 'class="dr-scope"' in page
    assert 'id="dr-styles"' in page
    assert f'id="{TW_SENTINEL_ID}"' in page
    assert f'{DATA_TW_READY}="false"' in page
    assert 'data-component="dr-hello"' in page
    assert "data-component" in page


def test_selectors_for_dump_include_ready_and_component_hooks() -> None:
    assert selectors_for_dump() == (
        '[data-tw-ready="true"]',
        "[data-component]",
    )


def test_bootstrap_tailwind_marks_tw_ready_sentinel() -> None:
    rendered = bootstrap_tailwind()
    assert TW_SENTINEL_ID in str(rendered)
    assert "dataset.twReady" in str(rendered)
