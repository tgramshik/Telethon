import asyncio
from telethon import TelegramClient
from telethon.tl.functions.payments import GetResaleStarGiftsRequest, GetPaymentFormRequest, SendStarsFormRequest
from telethon.tl.types import InputInvoiceStarGiftResale, InputPeerSelf

from telethon.tl.types import InputPeerUser

prices = { 
    5983471780763796287: 200, # santa hat 
    5936085638515261992: 3000, # signet ring / ring (дубликат) 
    5913442287462908725: 300, #spiced wine 
    5825895989088617224: 200, #hypno lolipop 
    6003373314888696650: 150, # candy cane 
    5773668482394620318: 200,   # egg 
    5868220813026526561: 2000,  # bear 
    5868659926187901653: 2000,  # bag 
    5936043693864651359: 2000,  # watch 
    5933629604416717361: 2500,  # shard 
    5933671725160989227: 2500,  # peach 
    5915521180483191380: 2000, # cap 
    5913517067138499193: 3000,  # perfume 
    5857140566201991735: 2000,  # cigare 
    5845776576658015084: 1000,  # frog 
    5843762284240831056: 3000,  # ion 
    5837059369300132790: 3000,  # cat 
    5936013938331222567: 25000, # pepe 
    5879737836550226478: 1500,  # oscar 
}

api_id = 6007208
api_hash = "fc242c751e4ffe3ae7f25ab4bfc25749"
client = TelegramClient("anon", api_id, api_hash)

async def buy_gift(gift_slug, gift_id):
    try:
        invoice = InputInvoiceStarGiftResale(
            slug=gift_slug,
            to_id=InputPeerUser(user_id=1399528718, access_hash=-201374014748859130) # @giftrelayer
        )
        form = await client(GetPaymentFormRequest(invoice=invoice))
        await client(SendStarsFormRequest(form_id=form.form_id, invoice=invoice))
        print(f"✅ Purchased gift with slug: {gift_slug}")
    except Exception as e:
        print(f"❌ Failed to buy gift {gift_slug}: {e}")

async def monitor_gift(gift_id, threshold):
    while True:
        try:
            offset = "0"
            while True:
                res = await client(GetResaleStarGiftsRequest(
                    gift_id=gift_id,
                    offset=offset,
                    limit=20,
                    sort_by_price=True,
                ))

                gifts = res.gifts
                if not gifts:
                    break

                for gift in gifts:
                    if gift.resell_stars <= threshold:
                        await buy_gift(gift.slug, gift_id)

        except Exception as e:
            print(f"⚠️ Error checking gift {gift_id}: {e}")

async def main():
    await client.start()
    tasks = [
        monitor_gift(gift_id, threshold)
        for gift_id, threshold in prices.items()
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
