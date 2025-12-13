export class Message {
  predictedCustomerId: string;

  @Prop({ required: true })
  content: string;
}
