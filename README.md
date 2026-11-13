# SchemaFirst A11y Standard

Deterministic accessibility rules for web pages and HTML email, built on WCAG 2.2 Level AA. Given the same subject and the same standard, two conforming evaluators report the same result for every automatable rule.

- Website: [www.schemafirst.org/standards/a11y](https://www.schemafirst.org/standards/a11y)
- Standard: [`standards/a11y/standard.json`](standards/a11y/standard.json), including its `rules`
- Schema: [`schemas/a11y-standard.schema.json`](schemas/a11y-standard.schema.json)
- Conformance cases: [`cases/`](cases/)

## Version 0.1.0 (draft)

0.1.0 is the first public draft. It uses the naming shared by all SchemaFirst standards: kebab-case keys and values, `rules` keyed by rule id, `requirement` of `required` / `recommended` / `optional`, provenance classes, an organization profile, and semver.

A subject conforms when every `required` rule that applies to it is `pass` or `not-applicable`. Each rule result is `pass`, `fail`, `not-applicable`, or `requires-review`. An evaluator never guesses a rule it cannot decide; it returns `requires-review`.

## Rules

50 rules: 33 required, 13 recommended, 4 optional. Every `wcag-defined` rule restates a WCAG 2.2 success criterion; `schemafirst-default` rules go beyond WCAG and never decide WCAG conformance.

| Rule | Name | Requirement | WCAG | Level | Applies to |
| --- | --- | --- | --- | --- | --- |
| `link-purpose` | Links say where they go | required | 2.4.4 | A | page, email |
| `control-names-unique` | Buttons and links are distinguishable | recommended | 2.4.6, 2.4.9 | AA | page, email |
| `plain-language` | Content uses plain language | optional | 3.1.5 | AAA | page, email |
| `text-alignment` | Body text is not justified | optional | 1.4.8 | AAA | page, email |
| `valid-markup` | Markup is well formed | recommended | — | none | page, email |
| `page-language` | Page declares its language | required | 3.1.1, 3.1.2 | AA | page, email |
| `page-title` | Page has a descriptive title | required | 2.4.2 | A | page |
| `viewport-zoom-enabled` | Zoom is not disabled | required | 1.4.4 | AA | page |
| `landmarks` | Page regions use landmarks | recommended | 1.3.1 | A | page |
| `bypass-blocks` | Repeated navigation can be skipped | recommended | 2.4.1 | A | page |
| `focus-order` | Focus order follows the layout | required | 2.4.3, 1.3.2 | A | page |
| `no-autofocus` | Focus is not moved on load | recommended | 2.4.3, 3.2.1 | A | page |
| `timing-adjustable` | Time limits can be extended | required | 2.2.1 | A | page |
| `no-title-tooltips` | Important information is not only in a title attribute | optional | — | none | page |
| `keyboard-operable` | Everything works from the keyboard | required | 2.1.1 | A | page |
| `no-keyboard-trap` | Keyboard focus is never trapped | required | 2.1.2 | A | page |
| `focus-visible` | Keyboard focus is visible | required | 2.4.7, 2.4.11 | AA | page |
| `no-hidden-focusable` | Hidden elements cannot receive focus | required | 2.4.3, 4.1.2 | A | page |
| `images-alt-present` | Images have an alt attribute | required | 1.1.1 | A | page, email |
| `alt-text-descriptive` | Alt text describes the image | required | 1.1.1 | A | page, email |
| `complex-images-described` | Charts and maps have a text alternative | recommended | 1.1.1 | A | page, email |
| `h1-present` | Page has one main heading | recommended | 1.3.1, 2.4.6 | AA | page |
| `heading-hierarchy` | Headings are in logical order | recommended | 1.3.1, 2.4.6 | AA | page, email |
| `lists-marked-up` | Lists use list markup | recommended | 1.3.1 | A | page, email |
| `data-tables-structured` | Data tables have headers | required | 1.3.1 | A | page, email |
| `aria-valid` | ARIA is used correctly | required | 4.1.2 | A | page, email |
| `links-distinguishable` | Links stand out from body text | required | 1.4.1 | A | page, email |
| `buttons-are-buttons` | Actions use buttons and navigation uses links | recommended | 4.1.2 | A | page |
| `form-labels` | Form fields are labelled | required | 1.3.1, 3.3.2, 4.1.2 | A | page |
| `error-identification` | Errors are identified and explained | required | 3.3.1, 3.3.3 | AA | page |
| `input-purpose` | Personal-data fields declare their purpose | required | 1.3.5 | AA | page |
| `video-captions` | Videos have captions | required | 1.2.2, 1.2.4 | AA | page, email |
| `audio-transcripts` | Audio has a transcript | required | 1.2.1 | A | page, email |
| `media-controls` | Media can be paused and audio does not autoplay | required | 1.4.2, 2.1.1 | A | page |
| `color-not-sole-indicator` | Color is not the only cue | required | 1.4.1 | A | page, email |
| `text-resize` | Text can be resized to 200% | required | 1.4.4 | AA | page, email |
| `reflow` | Content reflows at narrow widths | required | 1.4.10 | AA | page |
| `text-spacing` | Text spacing can be increased | required | 1.4.12 | AA | page |
| `body-font-size` | Body text is a readable size | recommended | — | none | page, email |
| `no-flashing` | Nothing flashes more than three times a second | required | 2.3.1 | A | page, email |
| `pause-stop-hide` | Moving content can be paused | required | 2.2.2 | A | page, email |
| `reduced-motion` | Animation respects reduced-motion preference | recommended | 2.3.3 | AAA | page |
| `text-contrast` | Text has enough contrast | required | 1.4.3 | AA | page, email |
| `non-text-contrast` | Controls and graphics have enough contrast | required | 1.4.11 | AA | page, email |
| `target-size` | Tap targets are large enough | required | 2.5.8 | AA | page |
| `orientation` | Content works in both orientations | required | 1.3.4 | AA | page |
| `pointer-gestures` | Gestures have a single-pointer alternative | required | 2.5.1, 2.5.7 | AA | page |
| `screen-reader-review` | Works with screen readers | required | 1.3.1, 4.1.2 | A | page, email |
| `email-images-off-legible` | Email is legible with images off | optional | — | none | email |
| `email-plain-text-part` | Email includes a plain-text part | recommended | — | none | email |

Rules with parameters (`text-contrast`, `non-text-contrast`, `target-size`, `body-font-size`, `reflow`, `pause-stop-hide`) state a default, a unit, and whether an organization may override it. For WCAG rules an override may only make the threshold stricter.

## Conformance

A conforming evaluator produces exactly the `expected` result for every rule listed in every file in `cases/`. The reference evaluator covers the code-analysis rules and validates the standard against its schema:

```bash
python3 scripts/check-conformance.py
```

Schema validation runs when the `jsonschema` package is installed.

## Lineage

0.1.0 merges two earlier SchemaFirst drafts and was reviewed against The A11Y Project Checklist. Rules marked `"a11y-project": true` correspond to a checklist item; the checklist's categories became `categories`.

From the January 2026 validation table (`accessibility-*` ids, `Critical` / `Major` severity):

| Earlier id | Rule |
| --- | --- |
| `accessibility-contrast-body` | `text-contrast` |
| `accessibility-contrast-large` | `text-contrast` |
| `accessibility-contrast-ui` | `non-text-contrast` |
| `accessibility-focus-visible` | `focus-visible` |
| `accessibility-color-not-sole` | `color-not-sole-indicator` |
| `accessibility-images-alt-present` | `images-alt-present` |
| `accessibility-alt-descriptive` | `alt-text-descriptive` |
| `accessibility-keyboard-nav` | `keyboard-operable` |
| `accessibility-no-keyboard-traps` | `no-keyboard-trap` |
| `accessibility-skip-links` | `bypass-blocks` |
| `accessibility-form-labels` | `form-labels` |
| `accessibility-aria-correct` | `aria-valid` |
| `accessibility-heading-hierarchy` | `heading-hierarchy` |
| `accessibility-lang-attribute` | `page-language` |
| `accessibility-screen-reader` | `screen-reader-review` |
| `accessibility-text-resize` | `text-resize` |
| `accessibility-no-flashing` | `no-flashing` |
| `accessibility-page-title` | `page-title` |
| `accessibility-h1-present` | `h1-present` |
| `accessibility-links-distinguishable` | `links-distinguishable` |

Severity `Critical` and `Major` are replaced by `requirement`, taken from the WCAG level: A and AA criteria are `required`. Two earlier `Critical` items changed: `h1-present` is `recommended` because WCAG does not require an h1, and `bypass-blocks` (formerly skip links) is satisfied by a skip link or a main landmark.

From the validation checks published in October 2026:

| Earlier check | Rule |
| --- | --- |
| `alt-text-on-images` | `images-alt-present`, `alt-text-descriptive` |
| `animation-respects-preferences` | `pause-stop-hide`, `reduced-motion` |
| `email-accessibility` | rules with `applies-to` email |
| `email-image-alt-text` | `images-alt-present`, `alt-text-descriptive` |
| `email-images-off-legibility` | `email-images-off-legible` |
| `email-plaintext-alt-present` | `email-plain-text-part` |
| `focus-indicators-visible` | `focus-visible` |
| `font-size-body-min-max` | `body-font-size` |
| `form-labels-associated` | `form-labels` |
| `keyboard-navigation-works` | `keyboard-operable` |
| `language-of-page` | `page-language` |
| `link-purpose` | `link-purpose` |
| `non-text-contrast` | `non-text-contrast` |
| `target-size` | `target-size` |
| `text-contrast` | `text-contrast` |
| `video-has-captions` | `video-captions` |

`non-text-contrast` and `target-size` were `recommended` in those checks; both are WCAG AA criteria and are `required` here. `body-font-size` defaults to 12 to 48 CSS px; the earlier check's 6 px minimum is raised.

Added after the A11Y Project review: `control-names-unique`, `plain-language`, `text-alignment`, `valid-markup`, `viewport-zoom-enabled`, `landmarks`, `focus-order`, `no-autofocus`, `timing-adjustable`, `no-title-tooltips`, `no-hidden-focusable`, `complex-images-described`, `lists-marked-up`, `data-tables-structured`, `buttons-are-buttons`, `error-identification`, `input-purpose`, `audio-transcripts`, `media-controls`, `reflow`, `text-spacing`, `orientation`, `pointer-gestures`.

## External basis

The W3C defines WCAG. SchemaFirst owns the rule ids, the deterministic checks, the default thresholds beyond WCAG, and the organization-profile model.

- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/WCAG22/Understanding/
- https://www.w3.org/WAI/ARIA/apg/
- https://www.a11yproject.com/checklist/

SchemaFirst is an independent community standard. It is not authored or endorsed by the W3C or The A11Y Project. Passing this standard's automated rules does not by itself make a site accessible; `manual-review` rules exist for that reason.

## License

Apache License 2.0. See [LICENSE](LICENSE), [NOTICE](NOTICE), and [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).
