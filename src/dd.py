

import tensorflow as tf 
from tensorflow.keras.layers import Conv2D, Conv2DTranspose, Concatenate, LeakyReLU


def base_model(include_top=False,net_name='DenseNet169'):
    # base = tf.keras.applications.net_na(input_shape=(None,None,3),include_top=include_top)
    
    if net_name=='DenseNet169':
        base = tf.keras.applications.DenseNet169(input_shape=(480,640,3),include_top=include_top)

    elif net_name=='DenseNet201':
        base = tf.keras.applications.DenseNet201(input_shape=(480,640,3),include_top=include_top)

    return base


# def encoder_layer(last_layer,filters,name,concat_with)

def get_decoder(tensor,filters,concat_with_tensor,layer_name,enable_skip=True):
    # decoder = Conv2DTranspose(filters=filters,
                            #   kernel_size=(80,60),
                            #   padding='valid')(tensor)
    
    _,h,w,_ = tensor.shape
   
    decoder  = tf.image.resize_images(tensor,[2*h,2*w],method=tf.image.ResizeMethod.BILINEAR,align_corners=False)

    if enable_skip:

        decoder = Concatenate(name="conv_decode_concat"+layer_name)([decoder,concat_with_tensor])
    
    decoder = Conv2D(filters=filters,
                     kernel_size=3,
                     padding='same',
                     name='convA_decoder_'+layer_name)(decoder)

    decoder = LeakyReLU(alpha=0.2)(decoder)

    decoder = Conv2D(filters=filters,
                     kernel_size=3,
                     padding='same',
                     name='convB_decoder_'+layer_name)(decoder)

    decoder = LeakyReLU(alpha=0.2)(decoder)

    return decoder

def get_dd():
    base = base_model()
    i = 0
    for layer in base.layers:
        layer.trainable = True
        # print(layer.name,layer.output.shape)
        # i += 1
        # if i>=11 and i<21:
        #     print(layer.name,layer.output.shape) 
        # elif i==21:
        #     break

    decoder = Conv2D(filters=base.layers[-1].output.shape[-1],
                                     kernel_size=1,
                                     padding='same',
                                     input_shape=base.layers[-1].output.shape,
                                     name='conv_decoder_up1')(base.output)
    
    decoder = get_decoder(tensor=decoder,
                          filters=base.layers[-1].output.shape[-1]//2,
                          concat_with_tensor=base.get_layer('pool3_pool').output,
                          layer_name='up1')
    
    decoder = get_decoder(tensor=decoder,
                          filters=base.layers[-1].output.shape[-1]//4,
                          concat_with_tensor=base.get_layer('pool2_pool').output,
                          layer_name='up2')
    
    decoder = get_decoder(tensor=decoder,
                          filters=base.layers[-1].output.shape[-1]//8,
                          concat_with_tensor=base.get_layer('pool1').output,
                          layer_name='up3')

    decoder = get_decoder(tensor=decoder,
                          filters=base.layers[-1].output.shape[-1]//16,
                          concat_with_tensor=base.get_layer('conv1/relu').output,
                          layer_name='up4')

    decoder = get_decoder(tensor=decoder,
                          filters=base.layers[-1].output.shape[-1]//32,
                          concat_with_tensor=base.get_layer('conv1/relu').output,
                          layer_name='up5',enable_skip=False)


    final_layer = Conv2D(filters=1,
                         kernel_size=3,
                         padding='same',
                         name='final_conv3')(decoder)

    model = tf.keras.Model(inputs=base.input,
                           outputs=final_layer)
   
    # print("Information about model")
    # print(model.output)
    return model

# if __name__ == "__main__":
#     model = get_dd()
#     model.summary()
    
