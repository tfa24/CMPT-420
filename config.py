from dataclasses import dataclass


@dataclass
class FinetuneConfig:
    max_length: int = 4096
    stride: int = 512
    per_device_train_batch_size: int = 1
    learning_rate: float = 2e-4
    lr_scheduler_type: str = "constant"
    optim: str = "adamw_bnb_8bit"
    gradient_accumulation_steps: int = 4
    max_grad_norm: float = 0.3
    lora_r: int = 32
    lora_target_modules: tuple[str] = (
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_up_proj",
        "down_proj",
    )
    lora_alpha: int = 16
    lora_dropout: float = 0.05
