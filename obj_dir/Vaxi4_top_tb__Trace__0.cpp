// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Tracing implementation internals
#include "verilated_vcd_c.h"
#include "Vaxi4_top_tb__Syms.h"


void Vaxi4_top_tb___024root__trace_chg_0_sub_0(Vaxi4_top_tb___024root* vlSelf, VerilatedVcd::Buffer* bufp);

void Vaxi4_top_tb___024root__trace_chg_0(void* voidSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root__trace_chg_0\n"); );
    // Init
    Vaxi4_top_tb___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vaxi4_top_tb___024root*>(voidSelf);
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    if (VL_UNLIKELY(!vlSymsp->__Vm_activity)) return;
    // Body
    Vaxi4_top_tb___024root__trace_chg_0_sub_0((&vlSymsp->TOP), bufp);
}

void Vaxi4_top_tb___024root__trace_chg_0_sub_0(Vaxi4_top_tb___024root* vlSelf, VerilatedVcd::Buffer* bufp) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root__trace_chg_0_sub_0\n"); );
    // Init
    uint32_t* const oldp VL_ATTR_UNUSED = bufp->oldp(vlSymsp->__Vm_baseCode + 1);
    // Body
    if (VL_UNLIKELY(vlSelf->__Vm_traceActivity[0U])) {
        bufp->chgIData(oldp+0,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__bins_hit),32);
        bufp->chgDouble(oldp+1,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__coverage_pct));
    }
    if (VL_UNLIKELY(vlSelf->__Vm_traceActivity[1U])) {
        bufp->chgIData(oldp+3,(vlSelf->axi4_top_tb__DOT__write_transaction_count),32);
        bufp->chgIData(oldp+4,(vlSelf->axi4_top_tb__DOT__read_transaction_count),32);
        bufp->chgIData(oldp+5,(vlSelf->axi4_top_tb__DOT__write_addr_handshake_count),32);
        bufp->chgIData(oldp+6,(vlSelf->axi4_top_tb__DOT__read_addr_handshake_count),32);
        bufp->chgIData(oldp+7,(vlSelf->axi4_top_tb__DOT__write_resp_handshake_count),32);
        bufp->chgIData(oldp+8,(vlSelf->axi4_top_tb__DOT__read_data_handshake_count),32);
        bufp->chgIData(oldp+9,(vlSelf->axi4_top_tb__DOT__assertion_pass_count),32);
        bufp->chgIData(oldp+10,(vlSelf->axi4_top_tb__DOT__assertion_fail_count),32);
        bufp->chgIData(oldp+11,(vlSelf->axi4_top_tb__DOT__warmup_cycles),32);
        bufp->chgBit(oldp+12,((1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles)));
        bufp->chgBit(oldp+13,(vlSelf->axi4_top_tb__DOT__awvalid_prev));
        bufp->chgBit(oldp+14,(vlSelf->axi4_top_tb__DOT__arvalid_prev));
        bufp->chgBit(oldp+15,(vlSelf->axi4_top_tb__DOT__wvalid_prev));
        bufp->chgBit(oldp+16,(vlSelf->axi4_top_tb__DOT__bvalid_prev));
        bufp->chgBit(oldp+17,(vlSelf->axi4_top_tb__DOT__rvalid_prev));
        bufp->chgBit(oldp+18,(vlSelf->axi4_top_tb__DOT__awready_prev));
        bufp->chgBit(oldp+19,(vlSelf->axi4_top_tb__DOT__arready_prev));
        bufp->chgBit(oldp+20,(vlSelf->axi4_top_tb__DOT__wready_prev));
        bufp->chgBit(oldp+21,(vlSelf->axi4_top_tb__DOT__bready_prev));
        bufp->chgBit(oldp+22,(vlSelf->axi4_top_tb__DOT__rready_prev));
        bufp->chgIData(oldp+23,(vlSelf->axi4_top_tb__DOT__total_aw_handshakes),32);
        bufp->chgIData(oldp+24,(vlSelf->axi4_top_tb__DOT__total_w_handshakes),32);
        bufp->chgIData(oldp+25,(vlSelf->axi4_top_tb__DOT__total_b_handshakes),32);
        bufp->chgIData(oldp+26,(vlSelf->axi4_top_tb__DOT__total_ar_handshakes),32);
        bufp->chgIData(oldp+27,(vlSelf->axi4_top_tb__DOT__total_r_handshakes),32);
        bufp->chgIData(oldp+28,(vlSelf->axi4_top_tb__DOT__total_wlast_seen),32);
        bufp->chgIData(oldp+29,(vlSelf->axi4_top_tb__DOT__total_rlast_seen),32);
        bufp->chgBit(oldp+30,(vlSelf->axi4_top_tb__DOT__awvalid_ever_seen));
        bufp->chgBit(oldp+31,(vlSelf->axi4_top_tb__DOT__arvalid_ever_seen));
        bufp->chgBit(oldp+32,(vlSelf->axi4_top_tb__DOT__wvalid_ever_seen));
        bufp->chgBit(oldp+33,(vlSelf->axi4_top_tb__DOT__bvalid_ever_seen));
        bufp->chgBit(oldp+34,(vlSelf->axi4_top_tb__DOT__rvalid_ever_seen));
        bufp->chgIData(oldp+35,(vlSelf->axi4_top_tb__DOT__write_beat_count),32);
        bufp->chgIData(oldp+36,(vlSelf->axi4_top_tb__DOT__write_burst_len),32);
        bufp->chgBit(oldp+37,(vlSelf->axi4_top_tb__DOT__write_burst_active));
        bufp->chgIData(oldp+38,(vlSelf->axi4_top_tb__DOT__read_beat_count),32);
        bufp->chgIData(oldp+39,(vlSelf->axi4_top_tb__DOT__read_burst_len),32);
        bufp->chgBit(oldp+40,(vlSelf->axi4_top_tb__DOT__read_burst_active));
        bufp->chgBit(oldp+41,(vlSelf->axi4_top_tb__DOT__aw_seen));
        bufp->chgBit(oldp+42,(vlSelf->axi4_top_tb__DOT__wlast_handshake_seen));
        bufp->chgIData(oldp+43,(vlSelf->axi4_top_tb__DOT__aw_timeout_counter),32);
        bufp->chgIData(oldp+44,(vlSelf->axi4_top_tb__DOT__w_timeout_counter),32);
        bufp->chgIData(oldp+45,(vlSelf->axi4_top_tb__DOT__pending_ar_count),32);
        bufp->chgIData(oldp+46,(vlSelf->axi4_top_tb__DOT__ar_no_data_counter),32);
        bufp->chgBit(oldp+47,(vlSelf->axi4_top_tb__DOT__ever_saw_rvalid));
        bufp->chgIData(oldp+48,(vlSelf->axi4_top_tb__DOT__ar_activity_counter),32);
        bufp->chgIData(oldp+49,(vlSelf->axi4_top_tb__DOT__aw_activity_counter),32);
        bufp->chgBit(oldp+50,(vlSelf->axi4_top_tb__DOT__ar_activity_checked));
        bufp->chgBit(oldp+51,(vlSelf->axi4_top_tb__DOT__aw_activity_checked));
        bufp->chgBit(oldp+52,(vlSelf->axi4_top_tb__DOT__reset_checked));
        bufp->chgIData(oldp+53,(vlSelf->axi4_top_tb__DOT__write_addr_low_count),32);
        bufp->chgIData(oldp+54,(vlSelf->axi4_top_tb__DOT__write_addr_mid_count),32);
        bufp->chgIData(oldp+55,(vlSelf->axi4_top_tb__DOT__write_addr_high_count),32);
        bufp->chgIData(oldp+56,(vlSelf->axi4_top_tb__DOT__write_burst_fixed_count),32);
        bufp->chgIData(oldp+57,(vlSelf->axi4_top_tb__DOT__write_burst_incr_count),32);
        bufp->chgIData(oldp+58,(vlSelf->axi4_top_tb__DOT__write_burst_wrap_count),32);
        bufp->chgIData(oldp+59,(vlSelf->axi4_top_tb__DOT__write_size_byte_count),32);
        bufp->chgIData(oldp+60,(vlSelf->axi4_top_tb__DOT__write_size_halfword_count),32);
        bufp->chgIData(oldp+61,(vlSelf->axi4_top_tb__DOT__write_size_word_count),32);
        bufp->chgIData(oldp+62,(vlSelf->axi4_top_tb__DOT__write_resp_okay_count),32);
        bufp->chgIData(oldp+63,(vlSelf->axi4_top_tb__DOT__write_resp_exokay_count),32);
        bufp->chgIData(oldp+64,(vlSelf->axi4_top_tb__DOT__write_resp_slverr_count),32);
        bufp->chgIData(oldp+65,(vlSelf->axi4_top_tb__DOT__write_resp_decerr_count),32);
        bufp->chgIData(oldp+66,(vlSelf->axi4_top_tb__DOT__read_addr_low_count),32);
        bufp->chgIData(oldp+67,(vlSelf->axi4_top_tb__DOT__read_addr_mid_count),32);
        bufp->chgIData(oldp+68,(vlSelf->axi4_top_tb__DOT__read_addr_high_count),32);
        bufp->chgIData(oldp+69,(vlSelf->axi4_top_tb__DOT__read_burst_fixed_count),32);
        bufp->chgIData(oldp+70,(vlSelf->axi4_top_tb__DOT__read_burst_incr_count),32);
        bufp->chgIData(oldp+71,(vlSelf->axi4_top_tb__DOT__read_burst_wrap_count),32);
        bufp->chgIData(oldp+72,(vlSelf->axi4_top_tb__DOT__read_resp_okay_count),32);
        bufp->chgIData(oldp+73,(vlSelf->axi4_top_tb__DOT__read_resp_exokay_count),32);
        bufp->chgIData(oldp+74,(vlSelf->axi4_top_tb__DOT__read_resp_slverr_count),32);
        bufp->chgIData(oldp+75,(vlSelf->axi4_top_tb__DOT__read_resp_decerr_count),32);
        bufp->chgIData(oldp+76,(vlSelf->axi4_top_tb__DOT__aw_handshake_valid_ready_count),32);
        bufp->chgIData(oldp+77,(vlSelf->axi4_top_tb__DOT__w_handshake_valid_ready_count),32);
        bufp->chgIData(oldp+78,(vlSelf->axi4_top_tb__DOT__b_handshake_valid_ready_count),32);
        bufp->chgIData(oldp+79,(vlSelf->axi4_top_tb__DOT__ar_handshake_valid_ready_count),32);
        bufp->chgIData(oldp+80,(vlSelf->axi4_top_tb__DOT__r_handshake_valid_ready_count),32);
        bufp->chgIData(oldp+81,(vlSelf->axi4_top_tb__DOT__interrupt_idle_count),32);
        bufp->chgIData(oldp+82,(vlSelf->axi4_top_tb__DOT__interrupt_pending_count),32);
        bufp->chgIData(oldp+83,(vlSelf->axi4_top_tb__DOT__interrupt_acknowledged_count),32);
        bufp->chgBit(oldp+84,(vlSelf->axi4_top_tb__DOT__interrupt_req_prev));
        bufp->chgBit(oldp+85,(vlSelf->axi4_top_tb__DOT__interrupt_ack_prev));
        bufp->chgIData(oldp+86,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_fixed_count),32);
        bufp->chgIData(oldp+87,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_incr_count),32);
        bufp->chgIData(oldp+88,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_wrap_count),32);
        bufp->chgIData(oldp+89,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_write_count),32);
        bufp->chgIData(oldp+90,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_write_count),32);
        bufp->chgIData(oldp+91,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_read_count),32);
        bufp->chgIData(oldp+92,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_read_count),32);
        bufp->chgIData(oldp+93,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count),32);
        bufp->chgIData(oldp+94,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count),32);
        bufp->chgIData(oldp+95,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count),32);
        bufp->chgIData(oldp+96,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count),32);
        bufp->chgIData(oldp+97,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__aw_handshake_count),32);
        bufp->chgIData(oldp+98,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__w_handshake_count),32);
        bufp->chgIData(oldp+99,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__b_handshake_count),32);
        bufp->chgIData(oldp+100,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__ar_handshake_count),32);
        bufp->chgIData(oldp+101,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__r_handshake_count),32);
        bufp->chgIData(oldp+102,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region0_count),32);
        bufp->chgIData(oldp+103,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region1_count),32);
        bufp->chgIData(oldp+104,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region2_count),32);
        bufp->chgIData(oldp+105,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region3_count),32);
        bufp->chgIData(oldp+106,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_out_of_range_count),32);
        bufp->chgIData(oldp+107,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_full_count),32);
        bufp->chgIData(oldp+108,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_partial_count),32);
        bufp->chgIData(oldp+109,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wlast_asserted_count),32);
        bufp->chgIData(oldp+110,(vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__rlast_asserted_count),32);
    }
    if (VL_UNLIKELY(vlSelf->__Vm_traceActivity[2U])) {
        bufp->chgIData(oldp+111,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr),32);
        bufp->chgCData(oldp+112,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen),8);
        bufp->chgCData(oldp+113,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize),3);
        bufp->chgCData(oldp+114,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst),2);
        bufp->chgBit(oldp+115,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid));
        bufp->chgBit(oldp+116,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready));
        bufp->chgIData(oldp+117,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata),32);
        bufp->chgCData(oldp+118,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb),4);
        bufp->chgBit(oldp+119,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast));
        bufp->chgBit(oldp+120,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid));
        bufp->chgBit(oldp+121,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready));
        bufp->chgCData(oldp+122,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp),2);
        bufp->chgBit(oldp+123,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid));
        bufp->chgBit(oldp+124,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready));
        bufp->chgIData(oldp+125,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr),32);
        bufp->chgCData(oldp+126,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arlen),8);
        bufp->chgCData(oldp+127,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arsize),3);
        bufp->chgCData(oldp+128,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst),2);
        bufp->chgBit(oldp+129,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid));
        bufp->chgBit(oldp+130,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready));
        bufp->chgIData(oldp+131,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rdata),32);
        bufp->chgCData(oldp+132,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp),2);
        bufp->chgBit(oldp+133,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast));
        bufp->chgBit(oldp+134,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid));
        bufp->chgBit(oldp+135,(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready));
        bufp->chgBit(oldp+136,(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack));
        bufp->chgCData(oldp+137,(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__state),2);
        bufp->chgCData(oldp+138,(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__next_state),2);
        bufp->chgCData(oldp+139,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state),3);
        bufp->chgCData(oldp+140,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state),3);
        bufp->chgCData(oldp+141,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count),8);
        bufp->chgIData(oldp+142,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_base_addr),32);
        bufp->chgCData(oldp+143,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_length),8);
        bufp->chgCData(oldp+144,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_size),3);
        bufp->chgCData(oldp+145,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_burst),2);
        bufp->chgBit(oldp+146,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress));
        bufp->chgCData(oldp+147,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_count),8);
        bufp->chgIData(oldp+148,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_base_addr),32);
        bufp->chgCData(oldp+149,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_length),8);
        bufp->chgCData(oldp+150,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_size),3);
        bufp->chgCData(oldp+151,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_burst),2);
        bufp->chgBit(oldp+152,(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress));
        bufp->chgIData(oldp+153,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr),32);
        bufp->chgCData(oldp+154,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_len),8);
        bufp->chgCData(oldp+155,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size),3);
        bufp->chgCData(oldp+156,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_burst),2);
        bufp->chgBit(oldp+157,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr_accepted));
        bufp->chgCData(oldp+158,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count),8);
        bufp->chgBit(oldp+159,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress));
        bufp->chgBit(oldp+160,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted));
        bufp->chgBit(oldp+161,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending));
        bufp->chgBit(oldp+162,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_ready));
        bufp->chgIData(oldp+163,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr),32);
        bufp->chgIData(oldp+164,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__addr_offset),32);
        bufp->chgIData(oldp+165,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__byte_size),32);
        bufp->chgIData(oldp+166,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__wrap_boundary),32);
        bufp->chgIData(oldp+167,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__aligned_addr),32);
        bufp->chgIData(oldp+168,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__mem_addr),32);
        bufp->chgIData(oldp+169,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk2__DOT__read_addr),32);
    }
    bufp->chgBit(oldp+170,(vlSelf->axi4_top_tb__DOT__clk));
    bufp->chgBit(oldp+171,(vlSelf->axi4_top_tb__DOT__resetn));
    bufp->chgIData(oldp+172,(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk1__DOT__i),32);
}

void Vaxi4_top_tb___024root__trace_cleanup(void* voidSelf, VerilatedVcd* /*unused*/) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root__trace_cleanup\n"); );
    // Init
    Vaxi4_top_tb___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vaxi4_top_tb___024root*>(voidSelf);
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    // Body
    vlSymsp->__Vm_activity = false;
    vlSymsp->TOP.__Vm_traceActivity[0U] = 0U;
    vlSymsp->TOP.__Vm_traceActivity[1U] = 0U;
    vlSymsp->TOP.__Vm_traceActivity[2U] = 0U;
}
