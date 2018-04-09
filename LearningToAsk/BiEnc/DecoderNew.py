from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import torch.nn as nn
from torch.nn.utils.rnn import pad_packed_sequence, PackedSequence
from pytorch_misc import rnn_mask, packed_seq_iter, seq_lengths_from_pad, const_row


class DecoderLSTM(nn.Module):
    def __init__(self, encoder_hidden_dim, mlp_hidden_dim, decoder_hidden_dim=600, target_vocab_size=28000,
                 lstm_layers=2, target_embedding_dim=300):

        ############ NOTE ####################
        # 1. find mlp_hidden_dim. not given in paper
        # 2.
        # embedding, pad_idx, Wt_row_size, bos_token=0,
        #  eos_token=1, , decoder_dropout_prob=0.3, max_size=15, ):
        """
            Input Args:
                embeddings          : nn.Embedding Layer containing source_vocab_size * embedding_size
                encoder_hidden_dim  : Hidden Dimension of The Encoder (To be used for attention while Decoding)
                decoder_hidden_dim  : Hidden Dimension of The Decoder (To be used for attention while Decoding)
                pad_idx             : pad_idx for the embedding
                Wt_row_size         : Number of Rows in first layer(Ws) of classification module.
                (Column size is decoder_hidden_dim + encoder_hidden_dim)
                bos_token           : Beginning of Sentence token
                eos_token           : End of Sentence token
                decoder_layers      : Number of Layers in the Decoder
                decoder_dropout_prob: Dropout Ratio to be applied in the decoder LSTM hidden layers
                max_size            : Max size of the output sequence
            Note:
                1. Note that the Encoder and Decoder Vocabularies are of different sizes.
                    This is checked using assert condition using a self.vocab_size.
                    Check its Value.
                2. Encoder_hidden_dim is same as 2 * Hidden_Unit_Size of Encoder_LSTM.
                    (2 is due to Bidirectional Forward Pass and further Concatentation)
        """

        super(DecoderLSTM, self).__init__()
        self.target_vocab_size = target_vocab_size
        self.target_embed_dim = target_embedding_dim

        self.enc_h_dim = encoder_hidden_dim

        self.dec_h_dim = decoder_hidden_dim
        self.lstm_layers = lstm_layers

        self.dec_lstm = nn.LSTM(self.target_embed_dim, self.dec_h_dim, num_layers=self.lstm_layers,
                                batch_first=True, dropout=0.3)

    def forward(self, y_old, prev_state):

	print("PT1")
	print(y_old.size())
	print("PT2")
	print(prev_state[0].size())
	print(prev_state[1].size())
	print("PT3")
        output, H_new = self.dec_lstm(y_old, prev_state)

        h_new = H_new[0]
        c_new = H_new[1]

        # Since sequence length is 1 => h_new[1] == output

        return output, (h_new, c_new)
