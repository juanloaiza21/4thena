import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';

import { DatabaseService } from './database/database.service';
import { DatabaseModule } from './database/database.module';

import { AppConfigModule } from './config/config.module';
import { WhatsappModule } from './whatsapp/whatsapp.module';
import { NatsModule } from './nats/nats.module';

import { EmailsModule } from './emails/emails.module';
import { TwilioModule } from './twilio/twilio.module';

@Module({
  imports: [AppConfigModule, DatabaseModule, WhatsappModule, NatsModule, EmailsModule, TwilioModule],
  controllers: [AppController],
  providers: [AppService, DatabaseService],
})
export class AppModule { }
