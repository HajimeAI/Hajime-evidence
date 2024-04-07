use solana_program::{
    account_info::AccountInfo, entrypoint, entrypoint::ProgramResult, msg,
    program_error::ProgramError, pubkey::Pubkey,
};

use std::str::from_utf8;

entrypoint!(process_instruction);

pub fn process_instruction(
    _program_id: &Pubkey,
    _accounts: &[AccountInfo],
    _instruction_data: &[u8],
) -> ProgramResult {
    let string_result = from_utf8(_instruction_data);
    match string_result {
        Ok(s) => {
            msg!("hash:{}", s);
            Ok(())
        }
        Err(_) => {
            return Err(ProgramError::InvalidInstructionData);
        }
    }
}
