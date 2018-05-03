/**
 * <ins> and <s> tag plugin for markdown-it markdown parser with editor attributions.
 *
 * Original: https://github.com/brianjgeiger/markdown-it-ins-del/blob/1.0.0/index.js
 * Version: https://github.com/brianjgeiger/markdown-it-ins-del/releases/tag/1.0.0
 */

(function (root, factory) {
    if (typeof exports === "object") {
        module.exports = factory();
    } else {
        root.markdownitIns = factory();
    }
})(this, function () {

    "use strict";

    // parse sequence of markers,
    // "start" should point at a valid marker
    function scanDelims(state, start) {
        var pos = start, lastChar, nextChar, count,
            isLastWhiteSpace, isLastPunctChar,
            isNextWhiteSpace, isNextPunctChar,
            can_open = true,
            can_close = true,
            max = state.posMax,
            marker = state.src.charCodeAt(start),
            isWhiteSpace = state.md.utils.isWhiteSpace,
            isPunctChar = state.md.utils.isPunctChar,
            isMdAsciiPunct = state.md.utils.isMdAsciiPunct;

        // treat beginning of the line as a whitespace
        lastChar = start > 0 ? state.src.charCodeAt(start - 1) : 0x20;

        while (pos < max && state.src.charCodeAt(pos) === marker) { pos++; }

        if (pos >= max) {
            can_open = false;
        }

        count = pos - start;

        // treat end of the line as a whitespace
        nextChar = pos < max ? state.src.charCodeAt(pos) : 0x20;

        isLastPunctChar = isMdAsciiPunct(lastChar) || isPunctChar(String.fromCharCode(lastChar));
        isNextPunctChar = isMdAsciiPunct(nextChar) || isPunctChar(String.fromCharCode(nextChar));

        isLastWhiteSpace = isWhiteSpace(lastChar);
        isNextWhiteSpace = isWhiteSpace(nextChar);

        if (isNextWhiteSpace) {
            can_open = false;
        } else if (isNextPunctChar) {
            if (!(isLastWhiteSpace || isLastPunctChar)) {
                can_open = false;
            }
        }

        if (isLastWhiteSpace) {
            can_close = false;
        } else if (isLastPunctChar) {
            if (!(isNextWhiteSpace || isNextPunctChar)) {
                can_close = false;
            }
        }

        return {
            can_open: can_open,
            can_close: can_close,
            delims: count
        };
    }

    function insertweditor(state, silent) {
        var startCount,
            count,
            tagCount,
            found,
            stack,
            res,
            token,
            insertSuccess,
            max = state.posMax,
            start = state.pos,
            marker = state.src.charCodeAt(start);

        if (marker !== 0x2B  /* 0x2B = + */) { return false; }
        if (silent) { return false; } // don't run any pairs in validation mode

        res = scanDelims(state, start);
        startCount = res.delims;

        if (!res.can_open) {
            state.pos += startCount;
            // Earlier we checked !silent, but this implementation does not need it
            state.pending += state.src.slice(start, state.pos);
            return true;
        }

        stack = Math.floor(startCount / 2);
        if (stack <= 0) { return false; }
        state.pos = start + startCount;

        while (state.pos < max) {
            if (state.src.charCodeAt(state.pos) === marker) {
                res = scanDelims(state, state.pos);
                count = res.delims;
                tagCount = Math.floor(count / 2);
                if (res.can_close) {
                    if (tagCount >= stack) {
                        state.pos += count - 2;
                        found = true;
                        break;
                    }
                    stack -= tagCount;
                    state.pos += count;
                    continue;
                }

                if (res.can_open) { stack += tagCount; }
                state.pos += count;
                continue;
            }

            state.md.inline.skipToken(state);
        }

        if (!found) {
            // parser failed to find ending tag, so it's not valid emphasis
            state.pos = start;
            insertSuccess = false;
            return false;
        }

        // found!
        state.posMax = state.pos;
        state.pos = start + 2;

        // Earlier we checked !silent, but this implementation does not need it
        // state.push('ins_open', 'del', 1); change here for html open tag, and close tag down
        token        = state.push("ins_open", "ins", 1);
        token.markup = String.fromCharCode(marker) + String.fromCharCode(marker);

        state.md.inline.tokenize(state);

        token        = state.push("ins_close", "ins", -1);
        token.markup = String.fromCharCode(marker) + String.fromCharCode(marker);

        state.pos = state.posMax + 2;
        state.posMax = max;

        insertSuccess = true;

        // Adding editor as superscript after insert tag
        if (!insertSuccess) {
            return true;
        }
        var UNESCAPE_RE = /\\([ \\!"#$%&'()*+,.\/:;<=>?@[\]^_`{|}~-])/g;

        var foundStart,
            labelStart,
            content,
            token2,
            max2 = state.posMax,
            start2 = state.pos;

        if (state.src.charCodeAt(start2) !== 0x5B /* [ */) { return true; } // don't need to addeditor at all
        if (silent) { return false; } // don't run any pairs in validation mode
        if (start2 >= max2 || start2 + 2 >= max2) { return false; }

        state.pos = start2 + 1;

        while (state.pos < max2) {
            if (state.src.charCodeAt(state.pos) === 0x5D /* [ */) {
                foundStart = true;
                break;
            }
            state.md.inline.skipToken(state);
        }

        if (!foundStart || start2 + 1 === state.pos) {
            state.pos = start2;
            return false;
        }

        content = state.src.slice(start2 + 1, state.pos);

        // don't allow unescaped spaces/newlines inside
        if (content.match(/(^|[^\\])(\\\\)*\s/)) {
            state.pos = start2;
            return false;
        }

        // found!
        state.posMax = state.pos;
        labelStart = start2 + 1;
        state.pos = labelStart;

        // Earlier we checked !silent, but this implementation does not need it
        token2         = state.push("sup_open", "sup", 1);
        token2.markup  = "[";

        //token2         = state.push('text', '', 0);
        //token2.content = content.replace(UNESCAPE_RE, '$1');
        //token2.markup = String.fromCharCode(marker);

        state.md.inline.tokenize(state);

        token2         = state.push("sup_close", "sup", -1);
        token2.markup  = "]";

        state.pos = state.posMax+ 1;
        state.posMax = max2;

        return true;
    }

    function deleteweditor(state, silent) {
        var startCount,
            count,
            tagCount,
            found,
            stack,
            res,
            token,
            deleteSuccess,
            max = state.posMax,
            start = state.pos,
            marker = state.src.charCodeAt(start);

        if (marker !== 0x7E  /* 0x7E = ~ */) { return false; }
        if (silent) { return false; } // don't run any pairs in validation mode

        res = scanDelims(state, start);
        startCount = res.delims;

        if (!res.can_open) {
            state.pos += startCount;
            // Earlier we checked !silent, but this implementation does not need it
            state.pending += state.src.slice(start, state.pos);
            return true;
        }

        stack = Math.floor(startCount / 2);
        if (stack <= 0) { return false; }
        state.pos = start + startCount;

        while (state.pos < max) {
            if (state.src.charCodeAt(state.pos) === marker) {
                res = scanDelims(state, state.pos);
                count = res.delims;
                tagCount = Math.floor(count / 2);
                if (res.can_close) {
                    if (tagCount >= stack) {
                        state.pos += count - 2;
                        found = true;
                        break;
                    }
                    stack -= tagCount;
                    state.pos += count;
                    continue;
                }

                if (res.can_open) { stack += tagCount; }
                state.pos += count;
                continue;
            }

            state.md.inline.skipToken(state);
        }

        if (!found) {
        // parser failed to find ending tag, so it's not valid emphasis
            state.pos = start;
            deleteSuccess = false;
            return false;
        }

        // found!
        state.posMax = state.pos;
        state.pos = start + 2;

        // Earlier we checked !silent, but this implementation does not need it
        // state.push('ins_open', 's', 1); change here for html open tag, and close tag down
        token        = state.push("ins_open", "s", 1);
        token.markup = String.fromCharCode(marker) + String.fromCharCode(marker);

        state.md.inline.tokenize(state);

        token        = state.push("ins_close", "s", -1);
        token.markup = String.fromCharCode(marker) + String.fromCharCode(marker);

        state.pos = state.posMax + 2;
        state.posMax = max;

        deleteSuccess = true;

        // Adding editor as superscript after delete tag
        if (!deleteSuccess) {
            return true;
        }
        var UNESCAPE_RE = /\\([ \\!"#$%&'()*+,.\/:;<=>?@[\]^_`{|}~-])/g;

        var foundStart,
            labelStart,
            content,
            token2,
            max2 = state.posMax,
            start2 = state.pos;

        if (state.src.charCodeAt(start2) !== 0x5B /* [ */) { return true; } // don't need to addeditor at all
        if (silent) { return false; } // don't run any pairs in validation mode
        if (start2 >= max2 || start2 + 2 >= max2) { return false; }

        state.pos = start2 + 1;

        while (state.pos < max2) {
            if (state.src.charCodeAt(state.pos) === 0x5D /* [ */) {
                foundStart = true;
                break;
            }
            state.md.inline.skipToken(state);
        }

        if (!foundStart || start2 + 1 === state.pos) {
            state.pos = start2;
            return false;
        }

        content = state.src.slice(start2 + 1, state.pos);

        // don't allow unescaped spaces/newlines inside
        if (content.match(/(^|[^\\])(\\\\)*\s/)) {
            state.pos = start2;
            return false;
        }

        // found!
        state.posMax = state.pos;
        labelStart = start2 + 1;
        state.pos = labelStart;

        // Earlier checked !silent, but this implementation does not need it
        token2         = state.push("sup_open", "sup", 1);
        token2.markup  = "[";

        //token2         = state.push('text', '', 0);
        //token2.content = content.replace(UNESCAPE_RE, '$1');
        //token2.markup = String.fromCharCode(marker);

        state.md.inline.tokenize(state);

        token2         = state.push("sup_close", "sup", -1);
        token2.markup  = "]";

        state.pos = state.posMax+ 1;
        state.posMax = max2;

        return true;
    }

    return function(md) {
    // new rule will be added before this one, name of added rule, rule function.
        md.inline.ruler.before("emphasis", "ins", insertweditor);
        md.inline.ruler.before("emphasis", "s", deleteweditor);
    };

});
