// Kick Assembler starter smoke test.
// Build command depends on local Kick Assembler installation.

BasicUpstart2(start)

start:
    lda #$06
    sta $d020
    lda #$00
    sta $d021
    rts
